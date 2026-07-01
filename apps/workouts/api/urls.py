from django.urls import path

from apps.workouts.api.views import (
    ExerciseDetailAPIView,
    ExerciseListAPIView,
    WorkoutExerciseDetailAPIView,
    WorkoutExerciseListAPIView,
    WorkoutTemplateDetailAPIView,
    WorkoutTemplateListAPIView,
)

app_name = "workouts"

urlpatterns = [
    path(
        "exercises/",
        ExerciseListAPIView.as_view(),
        name="exercise-list",
    ),
    path(
        "exercises/<uuid:pk>/",
        ExerciseDetailAPIView.as_view(),
        name="exercise-detail",
    ),
    path(
        "workout-templates/",
        WorkoutTemplateListAPIView.as_view(),
        name="workout-template-list",
    ),
    path(
        "workout-templates/<uuid:pk>/",
        WorkoutTemplateDetailAPIView.as_view(),
        name="workout-template-detail",
    ),
    path(
        "workout-exercises/",
        WorkoutExerciseListAPIView.as_view(),
        name="workout-exercise-list",
    ),
    path(
        "workout-exercises/<uuid:pk>/",
        WorkoutExerciseDetailAPIView.as_view(),
        name="workout-exercise-detail",
    ),
]
