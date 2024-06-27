"""This module contains the base classes for single text and callback events."""

from typing import Any

from aiogram import F, MagicFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from aiogram_events.stepper import Entry
from aiogram_events.stepper.stepper import Stepper
from aiogram_events.utils.utils import reply_keyboard


# pylint: disable=R0903
class Team:
    """This is a simple class to store the user IDs of the admins and moderators.
    It's recommended to change the way of storing the user IDs based on the project requirements.
    And reimplement the is_admin and is_moderator methods in the child class of BaseEvent.
    But still, you can use this class as is.
    NOTE: This class won't somehow back up the user IDs, so if the bot restarts,
    the user IDs will be lost. Therefore, it's not recommended to use this class in production.

    Example:
        ```python
        from aiogram_events.event import Team

        Team.admins = [123456789]
        Team.moderators = [987654321]
        ```
    """

    admins: list[int] = []
    moderators: list[int] = []


class BaseEvent:
    """This is a base class for single text and callback events.

    Args:
        content (Message | CallbackQuery): The content of the event.
        state (FSMContext): The state of the event.

    Attributes:
        content (Message | CallbackQuery): The content of the event.
        state (FSMContext): The state of the event.
        user_id (int): The user ID of the event.
        by_admin (bool): True if the event is triggered by an admin, False otherwise.
        by_moderator (bool): True if the event is triggered by a moderator, False otherwise.
        answer (str | None): The answer to the event.
        entries (list[Entry] | None): The entries of the event.
        complete (str | None): Message which will be sent when entries are completed.
        menu (list[str] | None): The list of menu buttons of the event.
        admin_menu (list[str] | None): The list of admin menu buttons of the event.
        moderator_menu (list[str] | None): The list of moderator menu buttons of the event.
        results (dict[str, int | str] | None): The results of the event, where keys
            are the names of the entries and values are the answers.

    Public Methods:
        is_admin(user_id: int) -> bool: Check if the user is an admin.
        is_moderator(user_id: int) -> bool: Check if the user is a moderator.
        reply() -> None: Reply to the event.
        process(**kwargs) -> None: Process the event. Can be reimplemented in the child class.
            Or can be extended with additional logic by using super().process() in the child class.
            If the event has entries, it will start the stepper to process the entries.
            Through the **kwargs parameter, you can pass additional arguments to the stepper.
            Such as main_menu, cancel, and skip which are buttons for the stepper.
    """

    def is_admin(self, user_id: int) -> bool:
        """Check if the user is an admin.
        It's recommended to reimplement this method in the child class.

        Args:
            user_id (int): The user ID to check.

        Returns:
            bool: True if the user is an admin, False otherwise."""
        return user_id in Team.admins

    def is_moderator(self, user_id: int) -> bool:
        """Check if the user is a moderator.
        It's recommended to reimplement this method in the child class.

        Args:
            user_id (int): The user ID to check.

        Returns:
            bool: True if the user is a moderator, False otherwise."""
        return user_id in Team.moderators

    _answer: str | None = None
    _entries: list[Entry] | None = None
    _complete: str | None = None
    _menu: list[str] | None = None
    _admin_menu: list[str] | None = None
    _moderator_menu: list[str] | None = None
    _results: dict[str, int | str] | None = None

    def __init__(self, content: Message | CallbackQuery, state: FSMContext):
        self._content = content
        self._state = state
        user: User | None = content.from_user
        if user is None:
            raise ValueError("No user found in the content, can't create event.")
        self._user_id: int = user.id
        self._check_user()

    def _check_user(self) -> None:
        """Check required user roles and sets corresponding attributes.
        It can be reimplemented in the child class to set the user roles based on the
        project requirements.
        NOTE: If you'll add custom roles, you'll also need to reimplement the role_menu property.
        """
        self._by_admin = self.is_admin(self.user_id)
        self._by_moderator = self.is_moderator(self.user_id)

    @property
    def content(self) -> Message | CallbackQuery:
        """Returns the content of the event.

        Returns:
            Message | CallbackQuery: The content of the event."""
        return self._content

    @property
    def state(self) -> FSMContext:
        """Returns the state of the event.

        Returns:
            FSMContext: The state of the event."""
        return self._state

    @property
    def user_id(self) -> int:
        """Returns the user ID of the event.

        Returns:
            int: The user ID of the event."""
        return self._user_id

    @property
    def by_admin(self) -> bool:
        """Returns True if the event is triggered by an admin, False otherwise.

        Returns:
            bool: True if the event is triggered by an admin, False otherwise."""
        return self._by_admin

    @property
    def by_moderator(self) -> bool:
        """Returns True if the event is triggered by a moderator, False otherwise.

        Returns:
            bool: True if the event is triggered by a moderator, False otherwise."""
        return self._by_moderator

    @property
    def answer(self) -> str | None:
        """Returns the answer to the event.

        Returns:
            str | None: The answer to the event."""
        return self._answer

    @property
    def entries(self) -> list[Entry] | None:
        """Returns the entries of the event.

        Returns:
            list[Entry] | None: The entries of the event."""
        return self._entries

    @property
    def complete(self) -> str | None:
        """Returns a message which will be sent when entries are completed.

        Returns:
            str | None: The complete step of the event."""
        return self._complete

    @property
    def menu(self) -> list[str] | None:
        """Returns the list of menu buttons of the event.

        Returns:
            list[str] | None: The list of menu buttons of the event."""
        return self._menu

    @property
    def admin_menu(self) -> list[str] | None:
        """Returns the list of admin menu buttons of the event.

        Returns:
            list[str] | None: The list of admin menu buttons of the event."""
        return self._admin_menu

    @property
    def moderator_menu(self) -> list[str] | None:
        """Returns the list of moderator menu buttons of the event.

        Returns:
            list[str] | None: The list of moderator menu buttons of the event."""
        return self._moderator_menu

    @property
    def role_menu(self) -> list[str] | None:
        """Returns the menu buttons based on the user role.

        Returns:
            list[str] | None: The list of menu buttons based on the user role."""
        if self.by_admin and self.admin_menu is not None:
            return self.admin_menu
        if self.by_moderator and self.moderator_menu is not None:
            return self.moderator_menu
        return self.menu

    @property
    def results(self) -> dict[str, int | str] | None:
        """Returns the results of the event, where keys are the names of the entries and
        values are the answers.

        Returns:
            dict[str, int | str] | None: The results of the event."""
        return self._results

    @results.setter
    def results(self, value: dict[str, int | str] | None) -> None:
        """Sets the results of the event.

        Args:
            value (dict[str, int | str] | None): The results of the event."""
        self._results = value

    async def reply(self) -> None:
        """If the answer is set, reply to the event with the answer and the menu buttons."""
        if not self.answer:
            return
        await self.content.answer(self.answer, reply_markup=reply_keyboard(self.role_menu))

    async def process(self, **kwargs) -> None:
        """Process the event. Can be reimplemented in the child class.
        If working with entries, it's recommended to extend this method in the child class
        and use super().process() to add additional logic.

        Example:
            ```python

            class FormEvent(TextEvent):
                _button = BUTTON_FORM
                _complete = "Form completed."
                _entries = [
                    TextEntry("Name", "Incorrect name.", "Enter your name."),
                    TextEntry(
                        "Surname", "Incorrect surname.", "Enter your surname.", skippable=True),
                    NumberEntry("Age", "Incorrect age.", "Enter your age."),
                ]

                async def process(self) -> None:
                    await super().process(
                        main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL,skip=BUTTON_SKIP)

                    reply = ""
                    for field_name, answer in self.results.items():
                        reply += f"{field_name}: {answer}\n"
                    await self.content.answer(reply)
        ```
        """
        if self.entries:
            if not self.complete:
                raise ValueError("Complete step not set for the event.")

            stepper = Stepper(
                self.content,
                self.state,
                entries=self.entries,
                complete=self.complete,
                main_menu=kwargs.get("main_menu", None),
                cancel=kwargs.get("cancel", None),
                skip=kwargs.get("skip", None),
            )
            await stepper.start()
            self._results = await stepper.get_results()


class TextEvent(BaseEvent):
    """This is a base class for single text events.
    Each text event should have a _button attribute which is a string to filter the event.
    To answer the event, set the _answer attribute, if needed to update the menu
    buttons set the _menu attribute.
    NOTE: _answer property is required if _menu is set, since the Telegram API sents
        the menu buttons inside of the message. If the _answer is not set, the menu
        will not be displayed/updated.

    Example:
        ```python
        from aiogram_events.event import TextEvent

        class OptionsEvent(TextEvent):
            _button = BUTTON_OPTIONS
            _answer = "Options selected."
            _menu = [BUTTON_OPTION_1, BUTTON_OPTION_2, BUTTON_OPTION_3]

            async def process(self) -> None:
                await super().process()
        ```
    """

    _button: str | None = None

    @classmethod
    def button(cls) -> MagicFilter:
        """Returns a MagicFilter to filter the event by the button.

        Returns:
            MagicFilter: The MagicFilter to filter the event by the button."""
        return F.text == cls._button


class CallbackEvent(BaseEvent):
    """This is a base class for single callback events.
    Each callback event should have a _callback attribute which is a string to filter the event
    and a _data_type attribute which is a type of the data (e.g. int, str).
    It's important to mention that filter will check if the callback data starts with the
    _callback attribute, since usually the callback data is a combination of the _callback
    and the data.
    E.g. _callback = "admin__add_admin", data = 123, callback data = "admin__add_admin123".
    To answer the event, set the _answer attribute, if needed to update the menu
    buttons set the _menu attribute.
    NOTE: _answer property is required if _menu is set, since the Telegram API sents
        the menu buttons inside of the message. If the _answer is not set, the menu
        will not be displayed/updated.

    Example:
        ```python
        from aiogram_events.event import CallbackEvent, Team
        from aiogram_events.stepper import NumberEntry

        class AddAdmin(CallbackEvent):
            _callback = "admin__add_admin"
            _data_type = int
            _complete = "Admin added."

            _entries = [
                NumberEntry(
                    "Telegram ID", "Incorrect user ID.", "Enter the user Telegram ID to add it.")
            ]

            async def process(self) -> None:
                await super().process(
                    main_menu="Main Menu", cancel="Cancel", skip="Skip")
                if self.answers not in Team.admins:
                    Team.admins.append(self.answers)
        ```
    """

    _callback: str | None = None
    _data_type: type | None = None

    @classmethod
    def callback(cls) -> MagicFilter:
        """Returns a MagicFilter to filter the event by the callback.

        Returns:
            MagicFilter: The MagicFilter to filter the event by the callback."""
        return F.data.startswith(cls._callback)

    # pylint: disable=E1102
    def __init__(self, content: CallbackQuery, state: FSMContext) -> None:
        super().__init__(content, state)
        if not content.data:
            raise ValueError("Callback data is empty.")
        if not self._callback:
            raise ValueError("Callback prefix not set for CallbackEvent subclass.")
        if not self._data_type:
            raise ValueError("Data type not set for CallbackEvent subclass.")
        data = content.data.replace(self._callback, "")
        self._data = None if not data else self._data_type(data)

    @property
    def data(self) -> Any | None:
        """Returns the data of the event.

        Returns:
            Any | None: The data of the event."""
        return self._data

    # pylint: disable=E1133
    @property
    def answers(self) -> list[str | int] | str | int | None:
        """Returns the answers of the event.
        If list of entries contains only one entry, it will return the answer as a single value.
        Otherwise, it will return the answers as a list.
        In both cases, it only returns the answers of the entries, without the names.
        To get the answers with the names, use the results property.

        Returns:
            list[str | int] | str | int | None: The answers of the event.
        """
        if not self.entries:
            return None
        if not self.results:
            return None
        answers = []
        for entry in self.entries:
            answers.append(entry.get_answer(self.results))
        return answers if len(answers) > 1 else answers[0]
