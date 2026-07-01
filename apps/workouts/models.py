from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from apps.core.models import TenantAwareModel, TimeStampedModel
from apps.workouts.enums import Difficulty
from apps.workouts.managers import ExerciseManager

# ==========================================================
# Reference Models
# ==========================================================


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
        ordering = ("name",)

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
        ordering = ("name",)

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
        ordering = ("name",)

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
        ordering = ("name",)

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name


# ==========================================================
# Workout Models
# ==========================================================


class WorkoutTemplate(TenantAwareModel, TimeStampedModel):
    """
    Reusable workout template created by a trainer.
    """

    name = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )

    estimated_duration_minutes = models.PositiveSmallIntegerField(
        default=60,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_workout_templates",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=("tenant", "name"),
                name="uq_workout_template_name_per_tenant",
            ),
        ]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name


class WorkoutExercise(TimeStampedModel):
    """
    One exercise inside a workout template.
    """

    workout_template = models.ForeignKey(
        WorkoutTemplate,
        on_delete=models.CASCADE,
        related_name="workout_exercises",
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name="workout_exercises",
    )

    order = models.PositiveSmallIntegerField()

    sets = models.PositiveSmallIntegerField(
        default=3,
    )

    reps = models.PositiveSmallIntegerField(
        default=10,
    )

    rest_seconds = models.PositiveSmallIntegerField(
        default=60,
    )

    tempo = models.CharField(
        max_length=20,
        blank=True,
    )

    rpe = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ("order",)

        constraints = [
            models.UniqueConstraint(
                fields=("workout_template", "order"),
                name="uq_workout_exercise_order",
            ),
            models.UniqueConstraint(
                fields=("workout_template", "exercise"),
                name="uq_workout_exercise_unique",
            ),
        ]

        indexes = [
            models.Index(fields=["workout_template"]),
            models.Index(fields=["exercise"]),
            models.Index(fields=["order"]),
        ]

    def __str__(self) -> str:
        return f"{self.order}. {self.exercise.name}"
