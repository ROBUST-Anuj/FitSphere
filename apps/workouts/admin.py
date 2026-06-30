from django.contrib import admin

from apps.workouts.models import Equipment, Exercise, ExerciseCategory, MuscleGroup


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
