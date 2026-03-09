from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_reward_and_related_habit(habit):
    """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
    if habit.reward and habit.related_habit:
        raise ValidationError(
            _("Нельзя одновременно указать вознаграждение и связанную привычку")
        )


def validate_related_habit_is_pleasant(habit):
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(_("Связанная привычка должна быть приятной"))


def validate_pleasant_habit_no_reward_or_related(habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    if habit.is_pleasant and (habit.reward or habit.related_habit):
        raise ValidationError(
            _("У приятной привычки не может быть вознаграждения или связанной привычки")
        )


validate_pleasant_habit_no_reward_or_pleasant = (
    validate_pleasant_habit_no_reward_or_related
)
