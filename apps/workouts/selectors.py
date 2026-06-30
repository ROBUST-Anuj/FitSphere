from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.workouts.models import Equipment, Exercise, ExerciseCategory, MuscleGroup


def get_exercise_by_id(exercise_id: UUID) -> Exercise | None:
    """
    Return an exercise by its ID.
    """
    return Exercise.objects.active().filter(id=exercise_id).first()


def get_exercise_by_name(name: str) -> Exercise | None:
    """
    Return an exercise by name.
    """
    return Exercise.objects.active().filter(name__iexact=name).first()


def get_active_exercises() -> QuerySet[Exercise]:
    """
    Return all active exercises.
    """
    return Exercise.objects.active()


def get_beginner_exercises() -> QuerySet[Exercise]:
    return Exercise.objects.beginner()


def get_intermediate_exercises() -> QuerySet[Exercise]:
    return Exercise.objects.intermediate()


def get_advanced_exercises() -> QuerySet[Exercise]:
    return Exercise.objects.advanced()


def get_exercises_by_muscle_group(
    muscle_group: MuscleGroup,
) -> QuerySet[Exercise]:
    return Exercise.objects.by_muscle_group(
        muscle_group,
    )


def get_exercises_by_equipment(
    equipment: Equipment,
) -> QuerySet[Exercise]:
    return Exercise.objects.by_equipment(
        equipment,
    )


def get_exercises_by_category(
    category: ExerciseCategory,
) -> QuerySet[Exercise]:
    return Exercise.objects.by_category(
        category,
    )


def search_exercises(query: str):
    return Exercise.objects.search(query)


def get_inactive_exercises():
    return Exercise.objects.inactive()
