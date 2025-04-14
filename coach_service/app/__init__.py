# App initialization
import os
import redis
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Setup Redis for caching if REDIS_URL is provided
redis_client = None
if os.environ.get('REDIS_URL'):
    try:
        redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))
        redis_client.ping()  # Test connection
    except:
        redis_client = None

# Initialize Prometheus metrics
REQUEST_COUNT = Counter(
    'coach_service_request_count',
    'Coach Service Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'coach_service_request_latency_seconds',
    'Request latency in seconds',
    ['app_name', 'endpoint']
)
OPENAI_REQUEST_COUNT = Counter(
    'coach_service_openai_request_count',
    'OpenAI API Request Count',
    ['app_name', 'status']
)
OPENAI_REQUEST_LATENCY = Histogram(
    'coach_service_openai_request_latency_seconds',
    'OpenAI API Request Latency in seconds',
    ['app_name']
)
CACHE_HIT_COUNT = Counter(
    'coach_service_cache_hit_count',
    'Number of cache hits',
    ['app_name']
)
CACHE_MISS_COUNT = Counter(
    'coach_service_cache_miss_count',
    'Number of cache misses',
    ['app_name']
)

def create_wsgi_app(app):
    """Add Prometheus middleware to Flask app"""
    return DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })