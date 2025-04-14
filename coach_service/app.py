import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app import create_wsgi_app

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Add Prometheus metrics endpoint
    app.wsgi_app = create_wsgi_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=os.environ.get("DEBUG", "False").lower() == "true")