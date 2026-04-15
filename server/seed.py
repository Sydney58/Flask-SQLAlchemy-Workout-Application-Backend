#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date


def seed():
    """seed the database with sample data"""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # create some exercises
        exercise1 = Exercise(name='Bench Press', category='strength', equipment_needed=True)
        exercise2 = Exercise(name='Squat', category='strength', equipment_needed=True)
        exercise3 = Exercise(name='Push Up', category='strength', equipment_needed=False)
        exercise4 = Exercise(name='Running', category='cardio', equipment_needed=False)
        exercise5 = Exercise(name='Plank', category='balance', equipment_needed=False)

        db.session.add_all([exercise1, exercise2, exercise3, exercise4, exercise5])
        db.session.commit()

        # create some workouts
        workout1 = Workout(date=date(2024, 1, 15), duration_minutes=60, notes='Full body workout')
        workout2 = Workout(date=date(2024, 1, 16), duration_minutes=45, notes='Upper body focus')
        workout3 = Workout(date=date(2024, 1, 17), duration_minutes=30, notes='Cardio day')

        db.session.add_all([workout1, workout2, workout3])
        db.session.commit()

        # link exercises to workouts
        we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise1.id, sets=3, reps=10)
        we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise2.id, sets=3, reps=12)
        we3 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise3.id, sets=3, reps=15)
        we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=exercise1.id, sets=4, reps=8)
        we5 = WorkoutExercise(workout_id=workout2.id, exercise_id=exercise3.id, sets=3, reps=20)
        we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=exercise4.id, duration_seconds=1800)
        we7 = WorkoutExercise(workout_id=workout3.id, exercise_id=exercise5.id, duration_seconds=300)

        db.session.add_all([we1, we2, we3, we4, we5, we6, we7])
        db.session.commit()

        print('Seed data created successfully!')


if __name__ == '__main__':
    seed()