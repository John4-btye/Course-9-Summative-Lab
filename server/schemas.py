from marshmallow import Schema, fields, validates, ValidationError


# WorkoutExercise Schema 
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

    exercise = fields.Nested(
        "ExerciseSchema",
        exclude=("workout_exercises",)
    )

    @validates_schema
    def validate_workout_exercise(self, data, **kwargs):
        if not data.get("reps") and not data.get("duration_seconds"):
            raise ValidationError(
                "Must include either reps/sets or duration_seconds"
            )


# Exercise Schema
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    workout_exercises = fields.List(
        fields.Nested(
            "WorkoutExerciseSchema",
            exclude=("exercise",)
        )
    )

    @validates("name")
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Name must be at least 2 characters")


# Workout Schema
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()

    workout_exercises = fields.List(
        fields.Nested("WorkoutExerciseSchema")
    )

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0")