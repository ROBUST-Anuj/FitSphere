from __future__ import annotations

from django.db import models
from django.db.models import Q

from apps.workouts.enums import Difficulty


class ExerciseQuerySet(models.QuerySet):
    """
    Custom queryset for Exercise.
    """

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def beginner(self):
        return self.filter(
            difficulty=Difficulty.BEGINNER,
        )

    def intermediate(self):
        return self.filter(
            difficulty=Difficulty.INTERMEDIATE,
        )

    def advanced(self):
        return self.filter(
            difficulty=Difficulty.ADVANCED,
        )

    def by_muscle_group(self, muscle_group):
        return self.filter(
            muscle_group=muscle_group,
        )

    def by_equipment(self, equipment):
        return self.filter(
            equipment=equipment,
        )

    def by_category(self, category):
        return self.filter(
            category=category,
        )

    def search(self, query: str):
        return self.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(instructions__icontains=query)
        )


ExerciseManager = models.Manager.from_queryset(
    ExerciseQuerySet,
)
