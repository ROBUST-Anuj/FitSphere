from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.workouts.api.serializers import (
    ExerciseCreateSerializer,
    ExerciseReadSerializer,
    ExerciseUpdateSerializer,
    WorkoutExerciseCreateSerializer,
    WorkoutExerciseReadSerializer,
    WorkoutExerciseUpdateSerializer,
    WorkoutTemplateCreateSerializer,
    WorkoutTemplateReadSerializer,
    WorkoutTemplateUpdateSerializer,
)
from apps.workouts.filters import ExerciseFilter
from apps.workouts.models import Exercise, WorkoutExercise, WorkoutTemplate
from apps.workouts.services import ExerciseService, WorkoutExerciseService, WorkoutTemplateService


class ExerciseListAPIView(generics.ListCreateAPIView):
    """
    List active exercises and create new exercises.
    """

    queryset = Exercise.objects.active()

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_class = ExerciseFilter

    search_fields = (
        "name",
        "description",
        "instructions",
    )

    ordering_fields = (
        "name",
        "difficulty",
        "created_at",
    )

    ordering = ("name",)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ExerciseCreateSerializer

        return ExerciseReadSerializer

    def perform_create(self, serializer):
        ExerciseService.create_exercise(
            **serializer.validated_data,
        )


class ExerciseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or deactivate an exercise.
    """

    def get_queryset(self):
        return Exercise.objects.active()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ExerciseUpdateSerializer

        return ExerciseReadSerializer

    def perform_update(self, serializer):
        ExerciseService.update_exercise(
            exercise=self.get_object(),
            **serializer.validated_data,
        )

    def perform_destroy(self, instance):
        ExerciseService.deactivate_exercise(
            exercise=instance,
        )


class WorkoutTemplateListAPIView(generics.ListCreateAPIView):

    def get_queryset(self):
        return WorkoutTemplate.objects.filter(
            is_active=True,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkoutTemplateCreateSerializer

        return WorkoutTemplateReadSerializer

    def perform_create(self, serializer):
        WorkoutTemplateService.create_workout_template(
            **serializer.validated_data,
        )


class WorkoutTemplateDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):

    def get_queryset(self):
        return WorkoutTemplate.objects.filter(
            is_active=True,
        )

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return WorkoutTemplateUpdateSerializer

        return WorkoutTemplateReadSerializer

    def perform_update(self, serializer):
        WorkoutTemplateService.update_workout_template(
            workout_template=self.get_object(),
            **serializer.validated_data,
        )

    def perform_destroy(self, instance):
        WorkoutTemplateService.deactivate_workout_template(
            workout_template=instance,
        )


class WorkoutExerciseListAPIView(
    generics.ListCreateAPIView,
):

    def get_queryset(self):
        return WorkoutExercise.objects.select_related(
            "exercise",
            "workout_template",
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkoutExerciseCreateSerializer

        return WorkoutExerciseReadSerializer

    def perform_create(self, serializer):
        WorkoutExerciseService.add_exercise(
            **serializer.validated_data,
        )


class WorkoutExerciseDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):

    def get_queryset(self):
        return WorkoutExercise.objects.select_related(
            "exercise",
            "workout_template",
        )

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return WorkoutExerciseUpdateSerializer

        return WorkoutExerciseReadSerializer

    def perform_update(self, serializer):
        WorkoutExerciseService.update_workout_exercise(
            workout_exercise=self.get_object(),
            **serializer.validated_data,
        )

    def perform_destroy(self, instance):
        WorkoutExerciseService.remove_exercise(
            workout_exercise=instance,
        )
