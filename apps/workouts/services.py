from __future__ import annotations

from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.workouts.models import (
    Equipment,
    Exercise,
    ExerciseCategory,
    MuscleGroup,
    WorkoutExercise,
    WorkoutTemplate,
)

# ==========================================================
# Exercise
# ==========================================================


class ExerciseService:
    """
    Business logic for Exercise.
    """

    @staticmethod
    @transaction.atomic
    def create_exercise(
        *,
        name: str,
        description: str,
        instructions: str,
        muscle_group: MuscleGroup,
        equipment: Equipment,
        category: ExerciseCategory,
        difficulty: str,
        video_url: str = "",
    ) -> Exercise:
        """
        Create a new exercise.
        """

        if Exercise.objects.filter(
            name__iexact=name,
        ).exists():
            raise ValidationError(
                {
                    "name": [
                        "An exercise with this name already exists.",
                    ]
                }
            )

        return Exercise.objects.create(
            name=name,
            description=description,
            instructions=instructions,
            muscle_group=muscle_group,
            equipment=equipment,
            category=category,
            difficulty=difficulty,
            video_url=video_url,
        )

    @staticmethod
    @transaction.atomic
    def update_exercise(
        *,
        exercise: Exercise,
        **data,
    ) -> Exercise:
        """
        Update an existing exercise.
        """

        if (
            "name" in data
            and Exercise.objects.filter(
                name__iexact=data["name"],
            )
            .exclude(
                pk=exercise.pk,
            )
            .exists()
        ):
            raise ValidationError(
                {
                    "name": [
                        "An exercise with this name already exists.",
                    ]
                }
            )

        for field, value in data.items():
            setattr(
                exercise,
                field,
                value,
            )

        if data:
            exercise.save(
                update_fields=list(
                    data.keys(),
                )
            )

        return exercise

    @staticmethod
    @transaction.atomic
    def deactivate_exercise(
        *,
        exercise: Exercise,
    ) -> None:
        """
        Soft delete an exercise.
        """

        exercise.is_active = False

        exercise.save(
            update_fields=[
                "is_active",
            ]
        )

    @staticmethod
    @transaction.atomic
    def activate_exercise(
        *,
        exercise: Exercise,
    ) -> None:
        """
        Reactivate an exercise.
        """

        exercise.is_active = True

        exercise.save(
            update_fields=[
                "is_active",
            ]
        )


# ==========================================================
# Workout Template
# ==========================================================


class WorkoutTemplateService:
    """
    Business logic for WorkoutTemplate.
    """

    @staticmethod
    @transaction.atomic
    def create_workout_template(
        **validated_data,
    ) -> WorkoutTemplate:
        return WorkoutTemplate.objects.create(
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update_workout_template(
        *,
        workout_template: WorkoutTemplate,
        **validated_data,
    ) -> WorkoutTemplate:

        for field, value in validated_data.items():
            setattr(
                workout_template,
                field,
                value,
            )

        if validated_data:
            workout_template.save(
                update_fields=list(
                    validated_data.keys(),
                )
            )

        return workout_template

    @staticmethod
    @transaction.atomic
    def deactivate_workout_template(
        *,
        workout_template: WorkoutTemplate,
    ) -> None:

        workout_template.is_active = False

        workout_template.save(
            update_fields=[
                "is_active",
            ],
        )


# ==========================================================
# Workout Exercise
# ==========================================================


class WorkoutExerciseService:
    """
    Business logic for WorkoutExercise.
    """

    @staticmethod
    @transaction.atomic
    def add_exercise(
        *,
        workout_template: WorkoutTemplate,
        exercise: Exercise,
        order: int,
        sets: int,
        reps: int,
        rest_seconds: int = 60,
        tempo: str = "",
        rpe: float | None = None,
        notes: str = "",
    ) -> WorkoutExercise:

        return WorkoutExercise.objects.create(
            workout_template=workout_template,
            exercise=exercise,
            order=order,
            sets=sets,
            reps=reps,
            rest_seconds=rest_seconds,
            tempo=tempo,
            rpe=rpe,
            notes=notes,
        )

    @staticmethod
    @transaction.atomic
    def update_workout_exercise(
        *,
        workout_exercise: WorkoutExercise,
        **validated_data,
    ) -> WorkoutExercise:

        for field, value in validated_data.items():
            setattr(
                workout_exercise,
                field,
                value,
            )

        if validated_data:
            workout_exercise.save(
                update_fields=list(
                    validated_data.keys(),
                )
            )

        return workout_exercise

    @staticmethod
    @transaction.atomic
    def remove_exercise(
        *,
        workout_exercise: WorkoutExercise,
    ) -> None:

        workout_exercise.delete()

    @staticmethod
    @transaction.atomic
    def reorder_exercise(
        *,
        workout_exercise: WorkoutExercise,
        new_order: int,
    ) -> WorkoutExercise:

        workout_exercise.order = new_order

        workout_exercise.save(
            update_fields=[
                "order",
            ],
        )

        return workout_exercise
