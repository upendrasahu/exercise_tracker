import os
import json
import requests
import time
import hashlib
import functools
from flask import Blueprint, jsonify, request, g, render_template
from openai import OpenAI, RateLimitError
from app import (redis_client, REQUEST_COUNT, REQUEST_LATENCY,
                OPENAI_REQUEST_COUNT, OPENAI_REQUEST_LATENCY,
                CACHE_HIT_COUNT, CACHE_MISS_COUNT)

main = Blueprint('main', __name__)

# Get the exercise tracker service URL from environment variable or use default
EXERCISE_SERVICE_URL = os.environ.get('EXERCISE_SERVICE_URL', 'http://localhost:5000')

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Metrics decorator for route handlers
def track_request_metrics(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        request_start_time = time.time()

        # Execute the route handler
        response = f(*args, **kwargs)

        # Record request latency
        request_latency = time.time() - request_start_time
        endpoint = request.endpoint if request.endpoint else 'unknown'
        REQUEST_LATENCY.labels(app_name='coach_service', endpoint=endpoint).observe(request_latency)

        # Record request count
        status_code = response.status_code if hasattr(response, 'status_code') else 200
        REQUEST_COUNT.labels(
            app_name='coach_service',
            method=request.method,
            endpoint=endpoint,
            http_status=status_code
        ).inc()

        return response
    return decorated_function

def get_exercises(days=30):
    """Fetch exercises from the exercise tracker service"""
    try:
        response = requests.get(f"{EXERCISE_SERVICE_URL}/api/exercises?days={days}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch exercises: {str(e)}"}

def generate_advice(exercises):
    """Generate advice based on exercise data using OpenAI GPT"""
    if isinstance(exercises, dict) and "error" in exercises:
        return {"error": exercises["error"]}

    if not exercises or len(exercises) == 0:
        return {"error": "No exercises found in the selected time period. Please add some exercises first before requesting advice."}

    try:
        # Format the exercise data for the prompt
        exercise_summary = "\n".join([
            f"- {e['name']}: {e['sets']} sets of {e['reps']} reps at {e['weight']}kg on {e['date']}"
            for e in exercises if e.get('weight')
        ] + [
            f"- {e['name']}: {e['sets']} sets of {e['reps']} reps on {e['date']}"
            for e in exercises if not e.get('weight')
        ])

        # If after filtering, we have no valid exercises left
        if not exercise_summary:
            return {"error": "Could not format exercise data properly. Please check your exercise entries."}

        # Generate a prompt for the OpenAI API
        prompt = f"""Based on the following exercise log, provide personalized fitness advice,
        suggest improvements, and recommend a workout plan for the next week.
        Focus on progression, form, and recovery.

        Recent exercise history:
        {exercise_summary}
        """

        openai_start_time = time.time()

        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a knowledgeable fitness coach providing personalized advice based on workout data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Record OpenAI metrics
        openai_latency = time.time() - openai_start_time
        OPENAI_REQUEST_LATENCY.labels(app_name='coach_service').observe(openai_latency)
        OPENAI_REQUEST_COUNT.labels(app_name='coach_service', status='success').inc()

        advice = response.choices[0].message.content
        return {"advice": advice, "generated_at": time.time()}

    except RateLimitError:
        # Record rate limit errors
        OPENAI_REQUEST_COUNT.labels(app_name='coach_service', status='rate_limited').inc()
        return {"error": "OpenAI rate limit exceeded. Please try again later."}
    except Exception as e:
        # Record other errors
        OPENAI_REQUEST_COUNT.labels(app_name='coach_service', status='error').inc()
        return {"error": f"Failed to generate advice: {str(e)}"}

@main.route('/api/advice', methods=['GET'])
@track_request_metrics
def get_advice():
    days = request.args.get('days', default=30, type=int)

    # Check if we have cached advice
    cache_key = None
    if redis_client:
        # Create a hash of the request parameters for the cache key
        cache_key = f"advice:{hashlib.md5(f'days={days}'.encode()).hexdigest()}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            # Record cache hit
            CACHE_HIT_COUNT.labels(app_name='coach_service').inc()
            return jsonify(json.loads(cached_result))
        else:
            # Record cache miss
            CACHE_MISS_COUNT.labels(app_name='coach_service').inc()

    # Fetch exercises
    exercises = get_exercises(days)

    # Generate advice
    result = generate_advice(exercises)

    # Cache the result if we have Redis and the result is valid
    if redis_client and "error" not in result:
        redis_client.setex(
            cache_key,
            3600,  # Cache for 1 hour
            json.dumps(result)
        )

    return jsonify(result)

@main.route('/health', methods=['GET'])
@track_request_metrics
def health_check():
    return jsonify({"status": "healthy"})

@main.route('/metrics-info', methods=['GET'])
@track_request_metrics
def metrics_info():
    """Display information about available metrics for monitoring"""
    return render_template('metrics_info.html')