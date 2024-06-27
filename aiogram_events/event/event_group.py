"""This module contains base classes for grouping text and callback events."""

from typing import Type

from aiogram import F, MagicFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_events.event.event import CallbackEvent, TextEvent


class TextEventGroup:
    """This is a base class for grouping text events, should be used with text_events decorator.
    Each group should have a _events attribute with a list of text events.

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

    _events: list[Type[TextEvent]] | None = None

    @property
    def events(self) -> list[Type[TextEvent]] | None:
        """Returns a list of text events or None.

        Returns:
            list[Type[TextEvent]] | None: List of text events or None.
        """
        return self._events

    # pylint: disable=W0212, E1133
    @classmethod
    def buttons(cls) -> MagicFilter:
        """Returns a MagicFilter object to register a handler for multiple text events.

        Returns:
            MagicFilter: MagicFilter object.
        """
        if cls._events is None:
            raise ValueError("No events found in the group.")
        return F.text.in_([event._button for event in cls._events])

    # pylint: disable=W0212, E1133
    @classmethod
    def event(cls, message: Message, state: FSMContext) -> TextEvent | None:
        """Finds a text event in the group by the message text.

        Args:
            message (Message): Message object.
            state (FSMContext): FSMContext object.

        Returns:
            TextEvent | None: Text event or None."""
        if cls._events is None:
            raise ValueError("No events found in the group.")
        for event in cls._events:
            if event._button == message.text:
                return event(message, state)
        return None


class CallbackEventGroup:
    """This is a base class for grouping callback events, should be used with
    callback_event decorator.

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

    _events: list[Type[CallbackEvent]] | None = None
    _prefix: str | None = None

    @property
    def events(self) -> list[Type[CallbackEvent]] | None:
        """Returns a list of callback events or None.

        Returns:
            list[Type[CallbackEvent]] | None: List of callback events or None."""
        return self._events

    @property
    def prefix(self) -> str | None:
        """Returns a prefix for the group or None.

        Returns:
            str | None: Prefix for the group or None."""
        return self._prefix

    @classmethod
    def callbacks(cls) -> MagicFilter:
        """Returns a MagicFilter object to register a handler for multiple callback events.

        Returns:
            MagicFilter: MagicFilter object."""
        if cls._events is None or cls._prefix is None:
            raise ValueError("Events or prefix not found in the group.")
        return F.data.startswith(cls._prefix)

    # pylint: disable=W0212, E1133
    @classmethod
    def callback(cls, query: CallbackQuery, state: FSMContext) -> CallbackEvent | None:
        """Finds a callback event in the group by the query data.

        Args:
            query (CallbackQuery): CallbackQuery object.
            state (FSMContext): FSMContext object.

        Returns:
            CallbackEvent | None: Callback event or None."""
        if cls._events is None or cls._prefix is None:
            raise ValueError("Events or prefix not found in the group.")
        for event in cls._events:
            if event._callback is None:
                continue
            if query.data and query.data.startswith(event._callback):
                return event(query, state)
        return None
