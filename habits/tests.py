import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Habit
from datetime import time

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(8, 0),
            action='Утренняя зарядка',
            duration=60,
            is_public=True
        )

        self.assertEqual(habit.action, 'Утренняя зарядка')
        self.assertEqual(habit.place, 'Дом')
        self.assertEqual(habit.duration, 60)
        self.assertTrue(habit.is_public)
        self.assertEqual(str(habit), 'Утренняя зарядка в 08:00:00 в Дом')

    def test_habit_str_method(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time=time(18, 30),
            action='Прогулка',
            duration=120
        )
        expected_str = 'Прогулка в 18:30:00 в Парк'
        self.assertEqual(str(habit), expected_str)


class HabitAPITest(APITestCase):
    """Тесты API для привычек"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()

        self.habit_data = {
            'place': 'Офис',
            'time': '12:00:00',
            'action': 'Обеденный перерыв',
            'duration': 30,
            'is_public': False
        }

    def test_create_habit_authenticated(self):
        """Тест создания привычки с авторизацией"""
        self.client.force_authenticate(user=self.user)
        url = reverse('habit-list')
        response = self.client.post(url, self.habit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, 'Обеденный перерыв')

    def test_create_habit_without_user(self):
        """Тест создания привычки без указания пользователя (должен автоматически установиться)"""
        self.client.force_authenticate(user=self.user)
        url = reverse('habit-list')

        response = self.client.post(url, self.habit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.user, self.user)

    def test_list_habits(self):
        """Тест получения списка привычек"""
        Habit.objects.create(user=self.user, **self.habit_data)
        Habit.objects.create(
            user=self.user,
            place='Спортзал',
            time='19:00:00',
            action='Тренировка',
            duration=60
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_habit(self):
        """Тест получения конкретной привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)

        self.client.force_authenticate(user=self.user)
        url = reverse('habit-detail', args=[habit.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], habit.action)
        self.assertEqual(response.data['place'], habit.place)

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)

        self.client.force_authenticate(user=self.user)
        url = reverse('habit-detail', args=[habit.id])

        updated_data = self.habit_data.copy()
        updated_data['action'] = 'Обновленное действие'
        updated_data['place'] = 'Новое место'

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, 'Обновленное действие')
        self.assertEqual(habit.place, 'Новое место')

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)

        self.client.force_authenticate(user=self.user)
        url = reverse('habit-detail', args=[habit.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_access_other_user_habit(self):
        """Тест доступа к чужой привычке"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        habit = Habit.objects.create(
            user=other_user,
            place='Чужое место',
            time='10:00:00',
            action='Чужая привычка',
            duration=45
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('habit-detail', args=[habit.id])
        response = self.client.get(url)

        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN])


class PublicHabitTest(APITestCase):
    """Тесты для публичных привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        Habit.objects.create(
            user=self.user,
            place='Публичное место 1',
            time='09:00:00',
            action='Публичная привычка 1',
            duration=30,
            is_public=True
        )
        Habit.objects.create(
            user=self.user,
            place='Публичное место 2',
            time='10:00:00',
            action='Публичная привычка 2',
            duration=45,
            is_public=True
        )
        Habit.objects.create(
            user=self.user,
            place='Приватное место',
            time='11:00:00',
            action='Приватная привычка',
            duration=60,
            is_public=False
        )

    def test_public_habits_list(self):
        """Тест получения списка публичных привычек"""
        url = reverse('habit-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        for habit in response.data['results']:
            self.assertTrue(habit['is_public'])


class HabitValidationTest(TestCase):
    """Тесты валидации привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_duration_validation(self):
        """Тест валидации длительности (не больше 120 секунд)"""
        habit = Habit(
            user=self.user,
            place='Тест',
            time=time(12, 0),
            action='Тест',
            duration=120
        )
        habit.full_clean()

        habit.duration = 121
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_reward_and_related_habit_validation(self):
        """Тест валидации - нельзя выбрать и награду, и связанную привычку"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(20, 0),
            action='Чтение',
            duration=30,
            is_pleasant=True
        )

        habit = Habit(
            user=self.user,
            place='Офис',
            time=time(12, 0),
            action='Работа',
            duration=60,
            reward='Кофе',
            related_habit=pleasant_habit
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()