from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet

from apps.workouts.models import Exercise, WorkoutExercise, WorkoutTemplate

# ==========================================================
# Exercise
# ==========================================================


def get_exercise_by_id(
    exercise_id: UUID,
) -> Exercise | None:
    return (
        Exercise.objects.active()
        .filter(
            id=exercise_id,
        )
        .first()
    )


def get_active_exercises() -> QuerySet[Exercise]:
    return Exercise.objects.active()


def search_exercises(
    query: str,
) -> QuerySet[Exercise]:
    return Exercise.objects.search(query)


# ==========================================================
# WorkoutTemplate
# ==========================================================


def get_workout_template_by_id(
    template_id: UUID,
) -> WorkoutTemplate | None:
    return WorkoutTemplate.objects.filter(
        id=template_id,
        is_active=True,
    ).first()


def get_active_workout_templates() -> QuerySet[WorkoutTemplate]:
    return WorkoutTemplate.objects.filter(
        is_active=True,
    )


def search_workout_templates(
    query: str,
) -> QuerySet[WorkoutTemplate]:
    return WorkoutTemplate.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True,
    )


# ==========================================================
# WorkoutExercise
# ==========================================================


def get_workout_exercises(
    template: WorkoutTemplate,
) -> QuerySet[WorkoutExercise]:
    return (
        WorkoutExercise.objects.filter(
            workout_template=template,
        )
        .select_related(
            "exercise",
        )
        .order_by(
            "order",
        )
    )


def get_workout_exercise_by_id(
    workout_exercise_id: UUID,
) -> WorkoutExercise | None:
    return (
        WorkoutExercise.objects.select_related(
            "exercise",
            "workout_template",
        )
        .filter(
            id=workout_exercise_id,
        )
        .first()
    )
