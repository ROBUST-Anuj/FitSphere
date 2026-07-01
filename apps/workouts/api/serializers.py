from __future__ import annotations

from rest_framework import serializers

from apps.workouts.models import Exercise, WorkoutExercise, WorkoutTemplate

# ==========================================================
# Exercise
# ==========================================================


class ExerciseReadSerializer(serializers.ModelSerializer):
    muscle_group_name = serializers.CharField(
        source="muscle_group.name",
        read_only=True,
    )

    equipment_name = serializers.CharField(
        source="equipment.name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Exercise

        fields = (
            "id",
            "name",
            "description",
            "instructions",
            "muscle_group",
            "muscle_group_name",
            "equipment",
            "equipment_name",
            "category",
            "category_name",
            "difficulty",
            "video_url",
            "is_active",
            "created_at",
            "updated_at",
        )


class ExerciseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise

        fields = (
            "name",
            "description",
            "instructions",
            "muscle_group",
            "equipment",
            "category",
            "difficulty",
            "video_url",
        )


class ExerciseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise

        fields = (
            "description",
            "instructions",
            "muscle_group",
            "equipment",
            "category",
            "difficulty",
            "video_url",
            "is_active",
        )


# ==========================================================
# Workout Template
# ==========================================================


class WorkoutTemplateReadSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(
        source="created_by.email",
        read_only=True,
    )

    class Meta:
        model = WorkoutTemplate

        fields = (
            "id",
            "name",
            "description",
            "difficulty",
            "estimated_duration_minutes",
            "created_by",
            "created_by_email",
            "is_active",
            "created_at",
            "updated_at",
        )


class WorkoutTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate

        fields = (
            "name",
            "description",
            "difficulty",
            "estimated_duration_minutes",
            "created_by",
        )


class WorkoutTemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate

        fields = (
            "name",
            "description",
            "difficulty",
            "estimated_duration_minutes",
            "is_active",
        )


# ==========================================================
# Workout Exercise
# ==========================================================


class WorkoutExerciseReadSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(
        source="exercise.name",
        read_only=True,
    )

    class Meta:
        model = WorkoutExercise

        fields = (
            "id",
            "workout_template",
            "exercise",
            "exercise_name",
            "order",
            "sets",
            "reps",
            "rest_seconds",
            "tempo",
            "rpe",
            "notes",
            "created_at",
            "updated_at",
        )


class WorkoutExerciseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise

        fields = (
            "workout_template",
            "exercise",
            "order",
            "sets",
            "reps",
            "rest_seconds",
            "tempo",
            "rpe",
            "notes",
        )


class WorkoutExerciseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise

        fields = (
            "order",
            "sets",
            "reps",
            "rest_seconds",
            "tempo",
            "rpe",
            "notes",
        )
