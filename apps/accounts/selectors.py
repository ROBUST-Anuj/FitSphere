from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

if TYPE_CHECKING:
    from apps.accounts.models import User

UserModel = get_user_model()


def get_user_by_email(email: str) -> User | None:
    return UserModel.objects.filter(email__iexact=email).first()  # type: ignore[return-value]


def get_user_by_id(user_id: UUID) -> User | None:
    return UserModel.objects.filter(id=user_id).first()  # type: ignore[return-value]


def get_active_users() -> QuerySet[User]:
    return UserModel.objects.filter(is_active=True)  # type: ignore[return-value]


def email_exists(email: str) -> bool:
    return UserModel.objects.filter(email__iexact=email).exists()