from functools import wraps
from typing import Callable, Type

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import BaseEvent, CallbackEvent, TextEvent
from aiogram_events.event.event_group import CallbackEventGroup, TextEventGroup

router = Router()


def text_event(event: Type[TextEvent]) -> Callable:

    def decorator(func: Callable) -> Callable:

        @router.message(event.button())
        async def wrapper(message: Message, state: FSMContext) -> None:
            return await func(event(message, state))

        return wrapper

    return decorator


def text_events(events: TextEventGroup) -> Callable:

    def decorator(func: Callable) -> Callable:

        @router.message(events.buttons())
        async def wrapper(message: Message, state: FSMContext) -> None:

            return await func(events.event(message, state))

        return wrapper

    return decorator


def callback_event(callback: Type[CallbackEvent]) -> Callable:

    def decorator(func: Callable) -> Callable:

        @router.callback_query(callback.callback())
        async def wrapper(query: CallbackQuery, state: FSMContext) -> None:

            return await func(callback(query, state))

        return wrapper

    return decorator


def callback_events(callbacks: CallbackEventGroup) -> Callable:

    def decorator(func: Callable) -> Callable:

        @router.callback_query(callbacks.callbacks())
        async def wrapper(query: CallbackQuery, state: FSMContext) -> None:

            return await func(callbacks.callback(query, state))

        return wrapper

    return decorator


def admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to admin-only commands.
    If user of the event is not admin, log warning and return.

    Args:
        func (callable): Function to decorate.

    Returns:
        callable: Decorated function.
    """

    @wraps(func)
    async def wrapper(event: BaseEvent, *args, **kwargs) -> None:
        """Check if user is admin and call decorated function.

        Args:
            event (Event): Event object.
        """
        if event.is_admin:  # type: ignore[truthy-function]
            return await func(event, *args, **kwargs)
        else:
            return None

    return wrapper


def moderator_admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to commands which available for moderators and admins.
    If user of the event is not moderator or admin, log warning and return.

    Args:
        func (callable): Function to decorate.

    Returns:
        callable: Decorated function.
    """

    @wraps(func)
    async def wrapper(event: BaseEvent, *args, **kwargs) -> None:
        """Check if user is moderator or admin and call decorated function.

        Args:
            event (Event): Event object.
        """
        if event.is_moderator or event.is_admin:  # type: ignore[truthy-function]
            return await func(event, *args, **kwargs)
        else:
            return None

    return wrapper
