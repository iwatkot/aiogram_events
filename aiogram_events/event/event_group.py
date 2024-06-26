from typing import Type

from aiogram import F, MagicFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import CallbackEvent, TextEvent


class TextEventGroup:
    _events: list[Type[TextEvent]] | None = None

    @property
    def events(self) -> list[Type[TextEvent]] | None:
        return self._events

    @classmethod
    def buttons(cls) -> MagicFilter:
        if cls._events is None:
            raise ValueError("No events found in the group.")
        return F.text.in_([event._button for event in cls._events])

    @classmethod
    def event(cls, message: Message, state: FSMContext) -> TextEvent | None:
        if cls._events is None:
            raise ValueError("No events found in the group.")
        for event in cls._events:
            if event._button == message.text:
                return event(message, state)
        return None


class CallbackEventGroup:
    _events: list[Type[CallbackEvent]] | None = None
    _prefix: str | None = None

    @property
    def events(self) -> list[Type[CallbackEvent]] | None:
        return self._events

    @property
    def prefix(self) -> str | None:
        return self._prefix

    @classmethod
    def callbacks(cls) -> MagicFilter:
        if cls._events is None or cls._prefix is None:
            raise ValueError("Events or prefix not found in the group.")
        return F.data.startswith(cls._prefix)

    @classmethod
    def callback(cls, query: CallbackQuery, state: FSMContext) -> CallbackEvent | None:
        if cls._events is None or cls._prefix is None:
            raise ValueError("Events or prefix not found in the group.")
        for event in cls._events:
            if event._callback is None:
                continue
            if query.data and query.data.startswith(event._callback):
                return event(query, state)
        return None
