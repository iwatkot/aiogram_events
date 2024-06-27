"""This module contains utility functions and classes that are used in aiogram."""

from typing import Type

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def inline_keyboard(data: dict[str, str] | None = None) -> InlineKeyboardMarkup | None:
    """Returns an InlineKeyboardMarkup object with buttons.

    Args:
        data (dict[str, str]): Dictionary of buttons, where the key is the text and the value is
        the data

    Returns:
        InlineKeyboardMarkup: InlineKeyboardMarkup object with buttons or None if
            no buttons are provided."""
    if not data:
        return None
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=data)] for text, data in data.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def reply_keyboard(buttons: list[str] | None = None) -> ReplyKeyboardMarkup | None:
    """Returns a ReplyKeyboardMarkup object with buttons.

    Args:
        buttons (list[str]): List of buttons

    Returns:
        ReplyKeyboardMarkup: ReplyKeyboardMarkup object with buttons or None
            if no buttons are provided."""
    if not buttons:
        return None
    per_row = buttons_per_row(len(buttons))
    raw_keyboard = [buttons[i : i + per_row] for i in range(0, len(buttons), per_row)]
    keyboard = [[KeyboardButton(text=button) for button in row] for row in raw_keyboard]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def buttons_per_row(buttons: int) -> int:
    """Returns the number of buttons per row based on the number of buttons.

    Args:
        buttons (int): Number of buttons

    Returns:
        int: Number of buttons per row"""
    if buttons % 3 == 0 or buttons % 2 == 0:
        return buttons // 2 if buttons > 2 else buttons
    return buttons // 2 + buttons % 2


class FormMeta(type):
    """Simple class to set attributes as State objects without creating
    the instance of the class."""

    # pylint: disable=C0204
    def __new__(cls, name: str, bases: tuple, attrs: dict, steps: list[str] | None = None):
        if steps is None:
            steps = []
        for attr in steps:
            attrs[attr] = State()
        return super().__new__(cls, name, bases, attrs)


class CombinedMeta(FormMeta, type(StatesGroup)):  # type: ignore
    """Since the StatesGroup already has it's metaclass, we need to combine it
    with our metaclass."""


def get_form(steps: list[str]) -> Type[StatesGroup]:
    """Returns a new class, with attributes as State objects.

    Args:
        steps (list[str]): List of steps

    Returns:
        StatesGroup: New class with steps as State objects
    """

    # pylint: disable=R0903
    class Form(StatesGroup, metaclass=CombinedMeta, steps=steps):  # type: ignore
        """This class is used to create a form with multiple steps.
        It's not recommended to make any changes to this class."""

    return Form
