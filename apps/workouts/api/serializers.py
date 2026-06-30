from __future__ import annotations

from rest_framework import serializers

from apps.workouts.models import Exercise


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
