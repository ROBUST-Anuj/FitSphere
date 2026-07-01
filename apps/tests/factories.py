from __future__ import annotations

from django.contrib.auth import get_user_model

import factory

from apps.core.models import Tenant
from apps.workouts.enums import Difficulty
from apps.workouts.models import Equipment, Exercise, ExerciseCategory, MuscleGroup

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")

    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "Password@123"
        self.set_password(password)

        if create:
            self.save()


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    name = factory.Sequence(lambda n: f"Gym {n}")

    slug = factory.Sequence(lambda n: f"gym-{n}")


class MuscleGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MuscleGroup

    name = factory.Sequence(lambda n: f"Chest {n}")


class EquipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Equipment

    name = factory.Sequence(lambda n: f"Barbell {n}")


class ExerciseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseCategory

    name = factory.Sequence(lambda n: f"Push {n}")


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    name = factory.Sequence(lambda n: f"Bench Press {n}")

    description = "Compound chest exercise."

    instructions = "Press the bar upward."

    muscle_group = factory.SubFactory(MuscleGroupFactory)

    equipment = factory.SubFactory(EquipmentFactory)

    category = factory.SubFactory(ExerciseCategoryFactory)

    difficulty = Difficulty.BEGINNER

    video_url = "https://example.com/video"

    is_active = True
