from rest_framework import serializers

from .models import Habit
from .validators import (validate_pleasant_habit_no_reward_or_related,
                         validate_related_habit_is_pleasant,
                         validate_reward_and_related_habit)


class HabitSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "user_email",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]  # user остается read_only

    def validate(self, data):
        habit = Habit(**data) if not self.instance else self.instance

        if self.instance:
            for key, value in data.items():
                setattr(habit, key, value)

        validate_reward_and_related_habit(habit)
        validate_related_habit_is_pleasant(habit)
        validate_pleasant_habit_no_reward_or_related(habit)

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Habit
        fields = [
            "id",
            "user_email",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "duration",
            "is_public",
        ]
