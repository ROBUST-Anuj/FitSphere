from django.urls import path

from apps.workouts.api.views import ExerciseDetailAPIView, ExerciseListAPIView

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
]
