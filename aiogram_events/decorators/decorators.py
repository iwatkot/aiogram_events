from typing import Callable, Type

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import CallbackEvent, TextEvent
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
