from __future__ import annotations

import uuid

from django.db import models

from apps.core.models import TimeStampedModel
from apps.workouts.enums import Difficulty
from apps.workouts.managers import ExerciseManager


class MuscleGroup(TimeStampedModel):
    """
    Major muscle groups.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Equipment(TimeStampedModel):
    """
    Exercise equipment.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ExerciseCategory(TimeStampedModel):
    """
    Push, Pull, Legs, Cardio, Mobility...
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Exercise(TimeStampedModel):
    """
    Master exercise library.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    description = models.TextField()

    instructions = models.TextField(
        blank=True,
    )

    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.PROTECT,
        related_name="exercises",
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name="exercises",
    )

    category = models.ForeignKey(
        ExerciseCategory,
        on_delete=models.PROTECT,
        related_name="exercises",
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )

    video_url = models.URLField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = ExerciseManager()

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name
