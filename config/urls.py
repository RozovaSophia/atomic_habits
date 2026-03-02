from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version='v1',
        description="API для трекера полезных привычек",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@habittracker.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def home(request):
    html = """
    <h1>Добро пожаловать в Habit Tracker API!</h1>
    <ul>
        <li><a href="/admin/">Админ-панель</a></li>
        <li><a href="/swagger/">Swagger документация</a></li>
        <li><a href="/redoc/">ReDoc документация</a></li>
        <li><a href="/api/test/">Тест Users API</a></li>
        <li><a href="/habits/test/">Тест Habits API</a></li>
        <li><a href="/api/register/">Регистрация</a></li>
        <li><a href="/api/login/">Вход</a></li>
    </ul>
    """
    return HttpResponse(html)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('users.urls')),
    path('habits/', include('habits.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('telegram/', include('telegram.urls')),

    path('', home, name='home'),
]