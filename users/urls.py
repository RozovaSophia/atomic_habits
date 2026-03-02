from django.urls import path
from . import views

urlpatterns = [
    # Тестовые эндпоинты
    path('test/', views.TestView.as_view(), name='test'),
    path('test-post/', views.TestPostView.as_view(), name='test-post'),

    # Эндпоинты авторизации
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]