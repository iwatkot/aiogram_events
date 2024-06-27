"""This module contains decorators for event handlers."""

from functools import wraps
from typing import Callable, Type

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import BaseEvent, CallbackEvent, TextEvent
from aiogram_events.event.event_group import CallbackEventGroup, TextEventGroup

router = Router()


def text_event(event: Type[TextEvent]) -> Callable:
    """Decorator to register a handler for a single text event.
    Triggered by a message from _button attribute of the event.

    Args:
        event (Type[TextEvent]): Text event class.

    Returns:
        Callable: Decorator.

    Examples:
        ```python
        from aiogram_events.event import TextEvent
        from aiogram_events.decorators import text_event

        class StartEvent(TextEvent):
            _button = "/start"
            _answer = "Welcome to the bot!"
            _menu = ["Options", "Main Menu"]

        @text_event(StartEvent)
        async def start(event: TextEvent) -> None:
            await event.reply()
            await event.process()
        ```
    """

    def decorator(func: Callable) -> Callable:

        @router.message(event.button())
        async def wrapper(message: Message, state: FSMContext) -> None:
            return await func(event(message, state))

        return wrapper

    return decorator


def text_events(events: TextEventGroup) -> Callable:
    """Decorator to register a handler for multiple text events.
    Triggered by a message from _button attribute of any event.

    Args:
        events (TextEventGroup): Text event group class.

    Returns:
        Callable: Decorator.

    Examples:
        ```python
        from aiogram_events.event import TextEventGroup, TextEvent
        from aiogram_events.decorators import text_events

        class StartEvent(TextEvent):
            _button = "/start"
            _answer = "Welcome to the bot!"
            _menu = ["Options", "Main Menu"]

        class MainMenuEvent(TextEvent):
            _button = "Main Menu"
            _answer = "Now you are in the main menu."
            _menu = ["Form", "Main Menu"]

        class StartGroup(TextEventGroup):
            _events = [StartEvent, MainMenuEvent]

        @text_events(StartGroup)
        async def start(event: TextEvent) -> None:
            await event.reply()
            await event.process()
        ```

    """

    def decorator(func: Callable) -> Callable:

        @router.message(events.buttons())
        async def wrapper(message: Message, state: FSMContext) -> None:

            return await func(events.event(message, state))

        return wrapper

    return decorator


def callback_event(callback: Type[CallbackEvent]) -> Callable:
    """Decorator to register a handler for a single callback event.
    Triggered if callback data starts with _callback attribute of the event.

    Args:
        callback (Type[CallbackEvent]): Callback event class.

    Returns:
        Callable: Decorator.

    Examples:
        ```python
        from aiogram_events.event import CallbackEvent
        from aiogram_events.decorators import callback_event

        class StartEvent(CallbackEvent):
            _callback = "start"
            _data_type = str
            _answer = "Welcome to the bot!"

        @callback_event(StartEvent)
        async def start(event: CallbackEvent) -> None:
            await event.reply()
            await event.process()
        ```
    """

    def decorator(func: Callable) -> Callable:

        @router.callback_query(callback.callback())
        async def wrapper(query: CallbackQuery, state: FSMContext) -> None:

            return await func(callback(query, state))

        return wrapper

    return decorator


def callback_events(callbacks: CallbackEventGroup) -> Callable:
    """Decorator to register a handler for multiple callback events.
    Triggered if callback data starts with _prefix attribute of the group.

    Args:
        callbacks (CallbackEventGroup): Callback event group class.

    Returns:
        Callable: Decorator.

    Examples:
        ```python
        from aiogram_events.event import CallbackEventGroup, CallbackEvent
        from aiogram_events.decorators import callback_events

        class StartEvent(CallbackEvent):
            _callback = "base__start"
            _data_type = str
            _answer = "Welcome to the bot!"

        class MainMenuEvent(CallbackEvent):
            _callback = "base__main_menu"
            _data_type = str
            _answer = "Now you are in the main menu."

        class StartGroup(CallbackEventGroup):
            _events = [StartEvent, MainMenuEvent]
            _prefix = "base__"

        @callback_events(StartGroup)
        async def start(event: CallbackEvent) -> None:
            await event.reply()
            await event.process()
        ```
    """

    def decorator(func: Callable) -> Callable:

        @router.callback_query(callbacks.callbacks())
        async def wrapper(query: CallbackQuery, state: FSMContext) -> None:

            return await func(callbacks.callback(query, state))

        return wrapper

    return decorator


def admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to admin-only commands.

    Args:
        func (Callable): Function to decorate.

    Returns:
        Callable: Decorated function.

    Examples:
        ```python
        from aiogram_events.event import TextEvent
        from aiogram_events.decorators import admin_only

        SettingsEvent(TextEvent):
            _button = "Settings"
            _answer = "Settings menu."
            _menu = ["Options", "Main Menu"]

        @text_event(SettingsEvent)
        @admin_only
        async def settings(event: TextEvent) -> None:
            await event.reply()
            await event.process()
        ```
    """

    @wraps(func)
    async def wrapper(event: BaseEvent, *args, **kwargs) -> None:
        """Check if user is admin and call decorated function.

        Args:
            event (Event): Event object.
        """
        if event.is_admin:  # type: ignore[truthy-function]
            return await func(event, *args, **kwargs)

    return wrapper


def moderator_admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to commands which available for moderators and admins.

    Args:
        func (Callable): Function to decorate.

    Returns:
        callable: Decorated function.

    Examples:
        ```python
        from aiogram_events.event import TextEvent
        from aiogram_events.decorators import moderator_admin_only

        SettingsEvent(TextEvent):
            _button = "Settings"
            _answer = "Settings menu."
            _menu = ["Options", "Main Menu"]

        @text_event(SettingsEvent)
        @moderator_admin_only
        async def settings(event: TextEvent) -> None:
            await event.reply()
            await event.process()
        ```
    """

    @wraps(func)
    async def wrapper(event: BaseEvent, *args, **kwargs) -> None:
        """Check if user is moderator or admin and call decorated function.

        Args:
            event (Event): Event object.
        """
        if event.is_moderator or event.is_admin:  # type: ignore[truthy-function]
            return await func(event, *args, **kwargs)

    return wrapper
