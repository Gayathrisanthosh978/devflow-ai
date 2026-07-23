from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from apps.accounts.api.serializers.auth import RegisterSerializer,LoginSerializer
from drf_spectacular.utils import (OpenApiExample,OpenApiResponse,extend_schema)

@extend_schema(
    summary="Register a new user",
    description="Creates a new user account using email and password.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description="User registered successfully."
        ),
        400: OpenApiResponse(
            description="Validation error."
        ),
    },
    examples=[
        OpenApiExample(
            "Register Example",
            value={
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "Password@123",
                "confirm_password": "Password@123",
            },
        )
    ],
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="User Login",
    description="Authenticate a user and return JWT access and refresh tokens.",
    request=LoginSerializer,
)
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )