from app import create_app, db
from app.models import Exercise
from datetime import datetime, timedelta
import random

def add_dummy_data():
    """Add dummy exercise data for the last 30 days"""

    app = create_app()

    # Exercise types with their typical rep/set/weight ranges
    exercise_types = [
        {
            'name': 'Bench Press',
            'min_sets': 3, 'max_sets': 5,
            'min_reps': 5, 'max_reps': 12,
            'min_weight': 60, 'max_weight': 100,
        },
        {
            'name': 'Squats',
            'min_sets': 3, 'max_sets': 5,
            'min_reps': 5, 'max_reps': 12,
            'min_weight': 80, 'max_weight': 120,
        },
        {
            'name': 'Deadlift',
            'min_sets': 2, 'max_sets': 5,
            'min_reps': 3, 'max_reps': 8,
            'min_weight': 100, 'max_weight': 150,
        },
        {
            'name': 'Pull Ups',
            'min_sets': 3, 'max_sets': 5,
            'min_reps': 5, 'max_reps': 12,
            'min_weight': 0, 'max_weight': 0,  # Bodyweight exercise
        },
        {
            'name': 'Shoulder Press',
            'min_sets': 3, 'max_sets': 4,
            'min_reps': 8, 'max_reps': 12,
            'min_weight': 30, 'max_weight': 60,
        },
        {
            'name': 'Bicep Curls',
            'min_sets': 3, 'max_sets': 4,
            'min_reps': 10, 'max_reps': 15,
            'min_weight': 10, 'max_weight': 25,
        },
        {
            'name': 'Leg Press',
            'min_sets': 3, 'max_sets': 4,
            'min_reps': 8, 'max_reps': 12,
            'min_weight': 100, 'max_weight': 200,
        },
    ]

    # Notes to randomly select from
    possible_notes = [
        "Felt strong today",
        "Increased weight from last session",
        "Focused on form",
        "Slightly tired but pushed through",
        "Great pump",
        "Added an extra set",
        "Tried slower negatives",
        "Worked on mind-muscle connection",
        "",  # Empty note
        ""
    ]

    # Generate data for the last 30 days
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)

    current_date = start_date

    with app.app_context():
        # Check if we already have data for this period to avoid duplicates
        existing_exercises_count = Exercise.query.filter(
            Exercise.date >= start_date,
            Exercise.date <= end_date
        ).count()

        if existing_exercises_count > 0:
            print(f"Found {existing_exercises_count} existing exercises in the period. Skipping insertion to avoid duplicates.")
            return

        # Monday is 0, Sunday is 6
        workout_days = {
            0: ['Bench Press', 'Bicep Curls'],  # Monday: Chest and Arms
            1: ['Squats', 'Leg Press'],         # Tuesday: Legs
            2: ['Shoulder Press', 'Pull Ups'],  # Wednesday: Shoulders and Back
            3: ['Bench Press', 'Bicep Curls'],  # Thursday: Chest and Arms again
            4: ['Deadlift', 'Leg Press'],       # Friday: Back and Legs
            # Weekend rest, no workouts on 5 (Saturday) and 6 (Sunday)
        }

        print("Adding dummy exercise data...")
        exercises_added = 0

        while current_date <= end_date:
            # Get day of week as an integer (0 = Monday, 6 = Sunday)
            day_of_week = current_date.weekday()

            # Check if this is a workout day
            if day_of_week in workout_days:
                # Get exercises for this day
                day_exercises = workout_days[day_of_week]

                for exercise_name in day_exercises:
                    # Find the exercise type data
                    exercise_type = next((e for e in exercise_types if e['name'] == exercise_name), None)

                    if exercise_type:
                        sets = random.randint(exercise_type['min_sets'], exercise_type['max_sets'])
                        reps = random.randint(exercise_type['min_reps'], exercise_type['max_reps'])

                        # For bodyweight exercises, weight might be 0
                        if exercise_type['max_weight'] > 0:
                            weight = random.randint(exercise_type['min_weight'], exercise_type['max_weight'])
                        else:
                            weight = None

                        notes = random.choice(possible_notes)

                        # Create and add the exercise
                        exercise = Exercise(
                            name=exercise_name,
                            date=current_date,
                            sets=sets,
                            reps=reps,
                            weight=weight,
                            notes=notes
                        )

                        db.session.add(exercise)
                        exercises_added += 1

            current_date += timedelta(days=1)

        # Commit all exercises at once
        db.session.commit()
        print(f"Added {exercises_added} exercises over the last 30 days.")

if __name__ == "__main__":
    add_dummy_data()