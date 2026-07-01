import pytest
from rest_framework.test import APIClient

from apps.tests.factories import ExerciseFactory, TenantFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def tenant():
    return TenantFactory()


@pytest.fixture
def exercise():
    return ExerciseFactory()
