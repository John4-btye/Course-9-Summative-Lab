from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Workout, Exercise, WorkoutExercise
from server.schemas import WorkoutExerciseSchema, WorkoutSchema, ExerciseSchema
from marshmallow import ValidationError

app = Flask(__name__)

we_schema = WorkoutExerciseSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# Workout Routes
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    return workout_schema.dump(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}

    try:
        validated = workout_schema.load(data)
        workout = Workout(**validated)

        db.session.add(workout)
        db.session.commit()

        return workout_schema.dump(workout), 201

    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception:
        return {"error": "Server error"}, 500

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404
    
    db.session.delete(workout)
    db.session.commit()

    return {}, 204


# Exercise Routes
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    return exercise_schema.dump(exercise), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json() or {}

    try:
        validated = exercise_schema.load(data)
        exercise = Exercise(**validated)

        db.session.add(exercise)
        db.session.commit()

        return exercise_schema.dump(exercise), 201

    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception:
        return {"error": "Server error"}, 500

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return {}, 204


# Join Table Route
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json() or {}

    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return {"error": "Workout or Exercise not found"}, 404

    try:
        validated = we_schema.load(data)

        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated
        )

        db.session.add(we)
        db.session.commit()

        return we_schema.dump(we), 201

    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception:
        return {"error": "Server error"}, 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)