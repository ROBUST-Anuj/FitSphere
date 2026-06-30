"""
Authentication API Views.
"""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.api.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
)
from apps.accounts.permissions import IsAuthenticatedAndActive
from apps.accounts.services import AuthenticationService


class LoginView(GenericAPIView):

    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = AuthenticationService.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "access": result["access"],
                "refresh": result["refresh"],
                "user": UserSerializer(result["user"]).data,
            }
        )


class RefreshView(TokenRefreshView):
    """
    JWT Refresh endpoint.
    """

    pass


class LogoutView(GenericAPIView):

    permission_classes = [IsAuthenticatedAndActive]

    serializer_class = LogoutSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuthenticationService.logout(refresh_token=serializer.validated_data["refresh"])

        return Response(
            {"detail": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


class MeView(GenericAPIView):

    permission_classes = [IsAuthenticatedAndActive]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class ChangePasswordView(GenericAPIView):

    permission_classes = [IsAuthenticatedAndActive]

    serializer_class = ChangePasswordSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuthenticationService.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
