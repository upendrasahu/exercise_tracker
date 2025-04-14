from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g
from app.models import Exercise
from app import db, REQUEST_COUNT, REQUEST_LATENCY, DB_OPERATION_COUNT, ACTIVE_EXERCISES_COUNT
from datetime import datetime
import time
import functools
import os
import requests

main = Blueprint('main', __name__)

# Metrics decorator for route handlers
def track_request_metrics(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        request_start_time = time.time()
        g.request_start_time = request_start_time

        # Execute the route handler
        response = f(*args, **kwargs)

        # Record request latency
        request_latency = time.time() - request_start_time
        endpoint = request.endpoint if request.endpoint else 'unknown'
        REQUEST_LATENCY.labels(app_name='exercise_tracker', endpoint=endpoint).observe(request_latency)

        # Record request count
        status_code = response.status_code if hasattr(response, 'status_code') else 200
        REQUEST_COUNT.labels(
            app_name='exercise_tracker',
            method=request.method,
            endpoint=endpoint,
            http_status=status_code
        ).inc()

        return response
    return decorated_function

# Update exercise count metric
def update_exercise_count():
    count = Exercise.query.count()
    ACTIVE_EXERCISES_COUNT.set(count)

@main.route('/')
@track_request_metrics
def index():
    exercises = Exercise.query.order_by(Exercise.date.desc()).all()
    update_exercise_count()
    return render_template('index.html', exercises=exercises)

@main.route('/add', methods=['GET', 'POST'])
@track_request_metrics
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        date_str = request.form['date']
        sets = request.form['sets']
        reps = request.form['reps']
        weight = request.form['weight'] or None
        notes = request.form['notes']

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        exercise = Exercise(
            name=name,
            date=date,
            sets=sets,
            reps=reps,
            weight=weight,
            notes=notes
        )

        db.session.add(exercise)
        db.session.commit()

        # Track DB operation
        DB_OPERATION_COUNT.labels(
            app_name='exercise_tracker',
            operation='create',
            entity='exercise'
        ).inc()
        update_exercise_count()

        flash('Exercise added successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_exercise.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@track_request_metrics
def edit_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    if request.method == 'POST':
        exercise.name = request.form['name']
        exercise.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        exercise.sets = request.form['sets']
        exercise.reps = request.form['reps']
        exercise.weight = request.form['weight'] or None
        exercise.notes = request.form['notes']

        db.session.commit()

        # Track DB operation
        DB_OPERATION_COUNT.labels(
            app_name='exercise_tracker',
            operation='update',
            entity='exercise'
        ).inc()

        flash('Exercise updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit_exercise.html', exercise=exercise)

@main.route('/delete/<int:id>')
@track_request_metrics
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()

    # Track DB operation
    DB_OPERATION_COUNT.labels(
        app_name='exercise_tracker',
        operation='delete',
        entity='exercise'
    ).inc()
    update_exercise_count()

    flash('Exercise deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main.route('/api/exercises', methods=['GET'])
@track_request_metrics
def get_exercises():
    days = request.args.get('days', default=30, type=int)

    # Calculate the date range - get exercises from the past X days
    from datetime import datetime, timedelta
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    exercises = Exercise.query.filter(
        Exercise.date >= start_date,
        Exercise.date <= end_date
    ).order_by(Exercise.date.desc()).all()

    result = []
    for exercise in exercises:
        result.append({
            'id': exercise.id,
            'name': exercise.name,
            'date': exercise.date.strftime('%Y-%m-%d'),
            'sets': exercise.sets,
            'reps': exercise.reps,
            'weight': exercise.weight,
            'notes': exercise.notes
        })

    return jsonify(result)

@main.route('/metrics-info')
@track_request_metrics
def metrics_info():
    """Display information about available metrics for monitoring"""
    return render_template('metrics_info.html', title="Metrics Information")

@main.route('/coach-advice', methods=['GET'])
@track_request_metrics
def coach_advice():
    """Display the AI coach advice page"""
    days = request.args.get('days', default=30, type=int)

    # First check if we have any exercise data in the specified time period
    from datetime import timedelta
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    exercises = Exercise.query.filter(
        Exercise.date >= start_date,
        Exercise.date <= end_date
    ).count()

    if exercises == 0:
        # If no exercises exist in this date range, inform the user
        return render_template('coach_advice.html', advice=None, days=days,
                              error_message="No exercises found in the selected time period. Add some exercises first!")

    # Get the URL of the coach service
    coach_url = os.environ.get('COACH_SERVICE_URL', 'http://localhost:5001')

    try:
        # Call the coach service API with timeout to avoid long waits
        response = requests.get(f"{coach_url}/api/advice?days={days}", timeout=5)
        response.raise_for_status()
        advice_data = response.json()

        if "error" in advice_data:
            return render_template('coach_advice.html', advice=None, days=days,
                                  error_message=advice_data["error"])

        # Track successful API call
        DB_OPERATION_COUNT.labels(
            app_name='exercise_tracker',
            operation='read',
            entity='coach_advice'
        ).inc()

        return render_template('coach_advice.html', advice=advice_data.get('advice'), days=days)
    except requests.ConnectionError:
        # The most likely issue - Coach Service not running
        return render_template('coach_advice.html', advice=None, days=days,
                              error_message="Cannot connect to the Coach Service. Is it running on " + coach_url + "?")
    except requests.Timeout:
        return render_template('coach_advice.html', advice=None, days=days,
                              error_message="Coach Service request timed out. Try again later.")
    except requests.RequestException as e:
        return render_template('coach_advice.html', advice=None, days=days,
                              error_message=f"Error connecting to Coach Service: {str(e)}")