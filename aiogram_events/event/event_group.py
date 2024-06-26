from aiogram import F, MagicFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import CallbackEvent, TextEvent


class TextEventGroup:
    _events: list[TextEvent] | None = None

    @property
    def events(self) -> list[TextEvent] | None:
        return self._events

    @classmethod
    def buttons(cls) -> MagicFilter:
        if not isinstance(cls.events, list) or not cls.events:
            raise ValueError("No events found in the group.")
        return F.text.in_([event._button for event in cls.events])

    @classmethod
    def event(cls, message: Message, state: FSMContext) -> TextEvent | None:
        if not isinstance(cls.events, list) or not cls.events:
            raise ValueError("No events found in the group.")
        for event in cls.events:
            if event._button == message.text:
                return event(message, state)
        return None


class CallbackEventGroup:
    _events: list[CallbackEvent] | None = None
    _prefix: str | None = None

    @property
    def events(self) -> list[CallbackEvent] | None:
        return self._events

    @property
    def prefix(self) -> str | None:
        return self._prefix

    @classmethod
    def callbacks(cls) -> MagicFilter:
        if not isinstance(cls.events, list) or not cls.prefix:
            raise ValueError("Prefix not set for CallbackEventGroup.")
        return F.data.startswith(cls.prefix)

    @classmethod
    def callback(cls, query: CallbackQuery, state: FSMContext) -> CallbackEvent | None:
        if not isinstance(cls.events, list) or not cls.events:
            raise ValueError("No events found in the group.")
        if not cls.prefix:
            raise ValueError("Prefix not set for CallbackEventGroup.")
        for event in cls.events:
            if query.data and query.data.startswith(event.callback):
                return event(query, state)
        return None
