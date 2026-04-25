from server.app import app
from server.models import db, Workout, Exercise, WorkoutExercise
from datetime import date

with app.app_context():
    print("Seeding database...")

    # Reset DB
    db.drop_all()
    db.create_all()

    # Exercises
    e1 = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    e2 = Exercise(name="Squats", category="Strength", equipment_needed=False)
    e3 = Exercise(name="Running", category="Cardio", equipment_needed=False)

    # Workouts
    w1 = Workout(date=date.today(), duration_minutes=30, notes="Morning workout")
    w2 = Workout(date=date.today(), duration_minutes=45, notes="Leg day")

    # Join table entries
    we1 = WorkoutExercise(workout=w1, exercise=e1, reps=15, sets=3)
    we2 = WorkoutExercise(workout=w1, exercise=e3, duration_seconds=600)
    we3 = WorkoutExercise(workout=w2, exercise=e2, reps=12, sets=4)

    db.session.add_all([e1, e2, e3, w1, w2, we1, we2, we3])
    db.session.commit()

    print("Done seeding!")