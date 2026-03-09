from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """Авторизация пользователя"""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Необходимо указать username и password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(
                {"message": "Успешный вход", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """Выход из системы"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Выход выполнен успешно"}, status=status.HTTP_200_OK
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class TestView(APIView):
    """Тестовое представление"""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {"message": "Users API работает", "status": "success"},
            status=status.HTTP_200_OK,
        )


class TestPostView(APIView):
    """Тестовое представление для POST запросов"""

    permission_classes = [AllowAny]

    def post(self, request):
        return Response(
            {"message": "POST запрос работает", "data": request.data},
            status=status.HTTP_200_OK,
        )
