from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.TestHabitView.as_view(), name="habit-test"),
    path("habits/", views.HabitListCreateView.as_view(), name="habit-list"),
    path(
        "habits/<int:pk>/",
        views.HabitRetrieveUpdateDestroyView.as_view(),
        name="habit-detail",
    ),
    path("habits/public/", views.PublicHabitListView.as_view(), name="habit-public"),
]
