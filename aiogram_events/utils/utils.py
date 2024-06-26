from typing import Type

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def inline_keyboard(data: dict[str, str] | None = None) -> InlineKeyboardMarkup | None:
    if not data:
        return None
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=data)] for text, data in data.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def reply_keyboard(buttons: list[str] | None = None) -> ReplyKeyboardMarkup | None:
    if not buttons:
        return None
    per_row = buttons_per_row(len(buttons))
    raw_keyboard = [buttons[i : i + per_row] for i in range(0, len(buttons), per_row)]
    keyboard = [[KeyboardButton(text=button) for button in row] for row in raw_keyboard]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def buttons_per_row(buttons: int) -> int:
    if buttons % 3 == 0 or buttons % 2 == 0:
        return buttons // 2 if buttons > 2 else buttons
    else:
        return buttons // 2 + buttons % 2


class FormMeta(type):
    """Simple class to set attributes as State objects without creating the instance of the class."""

    def __new__(cls, name: str, bases: tuple, attrs: dict, steps: list[str] | None = None):
        if steps is None:
            steps = []
        for attr in steps:
            attrs[attr] = State()
        return super().__new__(cls, name, bases, attrs)


class CombinedMeta(FormMeta, type(StatesGroup)):  # type: ignore
    """Since the StatesGroup already has it's metaclass, we need to combine it with our metaclass."""

    pass


def get_form(steps: list[str]) -> Type[StatesGroup]:
    """Returns a new class, with attributes as State objects.

    Args:
        steps (list[str]): List of steps

    Returns:
        StatesGroup: New class with steps as State objects
    """

    class Form(StatesGroup, metaclass=CombinedMeta, steps=steps):  # type: ignore
        pass

    return Form
