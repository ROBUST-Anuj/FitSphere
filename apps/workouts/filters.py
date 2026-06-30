from __future__ import annotations

import django_filters

from apps.workouts.enums import Difficulty
from apps.workouts.models import Exercise


class ExerciseFilter(django_filters.FilterSet):
    """
    Filter set for Exercise.
    """

    difficulty = django_filters.ChoiceFilter(
        choices=Difficulty.choices,
    )

    muscle_group = django_filters.UUIDFilter(
        field_name="muscle_group__id",
    )

    equipment = django_filters.UUIDFilter(
        field_name="equipment__id",
    )

    category = django_filters.UUIDFilter(
        field_name="category__id",
    )

    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Exercise

        fields = (
            "difficulty",
            "muscle_group",
            "equipment",
            "category",
            "is_active",
        )
