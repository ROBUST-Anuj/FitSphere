from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.workouts.api.serializers import (
    ExerciseCreateSerializer,
    ExerciseReadSerializer,
    ExerciseUpdateSerializer,
)
from apps.workouts.filters import ExerciseFilter
from apps.workouts.models import Exercise
from apps.workouts.services import ExerciseService


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
