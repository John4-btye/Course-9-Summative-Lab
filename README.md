# Workout API Backend

## Overview

This project is a Flask-based REST API designed for a workout tracking application used by personal trainers. It allows users to create workouts, define exercises, and associate exercises with workouts including metrics like reps, sets, or duration.

---

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv

---

## Models

### Workout

- id (Primary Key)
- date (Date)
- duration_minutes (Integer)
- notes (Text)

### Exercise

- id (Primary Key)
- name (String)
- category (String)
- equipment_needed (Boolean)

### WorkoutExercise (Join Table)

- id (Primary Key)
- workout_id (Foreign Key)
- exercise_id (Foreign Key)
- reps (Integer)
- sets (Integer)
- duration_seconds (Integer)

---

## Relationships

- A Workout has many WorkoutExercises
- An Exercise has many WorkoutExercises
- A Workout has many Exercises through WorkoutExercises
- An Exercise has many Workouts through WorkoutExercises

---

## Validations

### Table Constraints

- Non-nullable fields enforced
- Foreign key constraints enforced

### Model Validations

- Workout duration must be greater than 0
- Exercise name must be at least 2 characters
- No negative values for reps, sets, or duration

### Schema Validations

- Workout duration must be positive
- Exercise name must be at least 2 characters
- WorkoutExercise requires either reps/sets or duration_seconds

---

## API Endpoints

### Workouts

- GET /workouts
- GET /workouts/<id>
- POST /workouts
- DELETE /workouts/<id>

### Exercises

- GET /exercises
- GET /exercises/<id>
- POST /exercises
- DELETE /exercises/<id>

### WorkoutExercises

- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

---

## Example Request

### Create Workout

POST /workouts
{
"date": "2026-04-25",
"duration_minutes": 30,
"notes": "Morning workout"
}

---

## Example Response

{
"id": 1,
"date": "2026-04-25",
"duration_minutes": 30,
"notes": "Morning workout",
"workout_exercises": []
}

---

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   pipenv install
3. Activate environment:
   pipenv shell
4. Set Flask app:
   export FLASK_APP=server.app
5. Run migrations:
   flask db upgrade
6. Seed database:
   python -m server.seed
7. Run server:
   flask run

---

## Notes

- This project does not include update endpoints as per lab requirements.
- Nested serialization is implemented to display exercises within workouts.
