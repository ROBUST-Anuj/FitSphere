"""
Authentication services.
"""

from __future__ import annotations

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationService:
    """
    Authentication business logic.
    """

    @staticmethod
    def login(
        *,
        email: str,
        password: str,
    ) -> dict:

        user = authenticate(
            username=email,
            password=password,
        )

        if user is None:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailed("Inactive account.")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def logout(
        *,
        refresh_token: str,
    ) -> None:

        token = RefreshToken(refresh_token)  # type: ignore[arg-type]
        token.blacklist()

    @staticmethod
    @transaction.atomic
    def change_password(
        *,
        user,
        old_password: str,
        new_password: str,
    ) -> None:

        if not user.check_password(old_password):
            raise ValidationError({"old_password": ["Incorrect password."]})

        validate_password(
            new_password,
            user,
        )

        user.set_password(new_password)

        user.save(update_fields=["password"])
