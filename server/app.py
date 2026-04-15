from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, Exercise, Workout, WorkoutExercise
from schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    data = workouts_schema.dump(workouts)
    return make_response(jsonify(data), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    exercises_data = []
    for we in workout.workout_exercises:
        exercises_data.append({
            'id': we.exercise.id,
            'name': we.exercise.name,
            'category': we.exercise.category,
            'equipment_needed': we.exercise.equipment_needed,
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        })
    
    data = workout_schema.dump(workout)
    data['exercises'] = exercises_data
    return make_response(jsonify(data), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return make_response(jsonify({'errors': errors}), 400)
    
    try:
        workout = workout_schema.load(data)
        db.session.add(workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(workout)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    try:
        WorkoutExercise.query.filter_by(workout_id=id).delete()
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({'message': 'Workout deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    data = exercises_schema.dump(exercises)
    return make_response(jsonify(data), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    workouts_data = []
    for we in exercise.workout_exercises:
        workouts_data.append({
            'id': we.workout.id,
            'date': we.workout.date.isoformat(),
            'duration_minutes': we.workout.duration_minutes,
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        })
    
    data = exercise_schema.dump(exercise)
    data['workouts'] = workouts_data
    return make_response(jsonify(data), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return make_response(jsonify({'errors': errors}), 400)
    
    try:
        exercise = exercise_schema.load(data)
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(exercise)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    try:
        WorkoutExercise.query.filter_by(exercise_id=id).delete()
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({'message': 'Exercise deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    
    data = request.get_json()
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id
    
    errors = workout_exercise_schema.validate(data)
    if errors:
        return make_response(jsonify({'errors': errors}), 400)
    
    try:
        workout_exercise = workout_exercise_schema.load(data)
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)