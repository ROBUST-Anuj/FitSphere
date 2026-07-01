from django.contrib import admin

from apps.workouts.models import (
    Equipment,
    Exercise,
    ExerciseCategory,
    MuscleGroup,
    WorkoutExercise,
    WorkoutTemplate,
)


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "muscle_group",
        "equipment",
        "category",
        "difficulty",
        "is_active",
    )

    list_filter = (
        "difficulty",
        "muscle_group",
        "equipment",
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    autocomplete_fields = (
        "muscle_group",
        "equipment",
        "category",
    )


# ==========================================================
# Workout Admin
# ==========================================================


class WorkoutExerciseInline(admin.TabularInline):
    """
    Edit workout exercises directly inside a workout template.
    """

    model = WorkoutExercise

    extra = 1

    autocomplete_fields = ("exercise",)

    ordering = ("order",)


@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "difficulty",
        "estimated_duration_minutes",
        "created_by",
        "is_active",
        "created_at",
    )

    list_filter = (
        "difficulty",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    autocomplete_fields = ("created_by",)

    inlines = (WorkoutExerciseInline,)


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "workout_template",
        "order",
        "exercise",
        "sets",
        "reps",
        "rest_seconds",
    )

    list_filter = ("workout_template",)

    autocomplete_fields = (
        "workout_template",
        "exercise",
    )

    ordering = (
        "workout_template",
        "order",
    )
