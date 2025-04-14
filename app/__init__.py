from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

# Initialize Prometheus metrics
REQUEST_COUNT = Counter(
    'exercise_tracker_request_count',
    'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'exercise_tracker_request_latency_seconds',
    'Request latency in seconds',
    ['app_name', 'endpoint']
)
DB_OPERATION_COUNT = Counter(
    'exercise_tracker_db_operation_count',
    'Database Operation Count',
    ['app_name', 'operation', 'entity']
)
ACTIVE_EXERCISES_COUNT = Gauge(
    'exercise_tracker_active_exercises_count',
    'Number of exercises in the database'
)

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Configure the SQLite database
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_exercise_tracker')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../exercise_data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Add Prometheus wsgi middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    return app