# Workout Application Backend

Flask backend API for tracking workouts and exercises.

## Setup

```bash
pipenv install
```

## Initialize Database

```bash
FLASK_APP=server.app:app flask db init
FLASK_APP=server.app:app flask db migrate -m 'Initial migration'
FLASK_APP=server.app:app flask db upgrade head
```

## Run

```bash
python server/seed.py
python server/app.py
```

API available at `http://localhost:5555`

## Endpoints

- GET /workouts - List all workouts
- GET /workouts/<id> - Get workout with exercises
- POST /workouts - Create workout
- DELETE /workouts/<id> - Delete workout
- GET /exercises - List all exercises
- GET /exercises/<id> - Get exercise with workouts
- POST /exercises - Create exercise
- DELETE /exercises/<id> - Delete exercise
- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add exercise to workout

## Validations

- Table constraint: duration_minutes > 0
- Table constraint: sets > 0
- Model validation: Exercise name required
- Model validation: Workout duration positive
- Schema validation: duration_minutes >= 1