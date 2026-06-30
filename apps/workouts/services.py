from __future__ import annotations

from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.workouts.models import Equipment, Exercise, ExerciseCategory, MuscleGroup


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

        if Exercise.objects.filter(name__iexact=name).exists():
            raise ValidationError({"name": ["An exercise with this name already exists."]})

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
            and Exercise.objects.filter(name__iexact=data["name"]).exclude(pk=exercise.pk).exists()
        ):
            raise ValidationError({"name": ["An exercise with this name already exists."]})

        for field, value in data.items():
            setattr(exercise, field, value)

        if data:
            exercise.save(update_fields=list(data.keys()))

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
