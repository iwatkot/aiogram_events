from abc import ABC, abstractmethod
from typing import Type

from aiogram import F, MagicFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from aiogram_events.stepper import Entry
from aiogram_events.stepper.stepper import Stepper
from aiogram_events.utils.utils import reply_keyboard


class BaseEvent(ABC):
    @abstractmethod
    def is_admin(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_moderator(self, user_id: int) -> bool:
        pass

    _answer: str | None = None
    _entries: list[Type[Entry]] | None = None
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
        self._by_admin = self.is_admin(self.user_id)
        self._by_moderator = self.is_moderator(self.user_id)

    @property
    def content(self) -> Message | CallbackQuery:
        return self._content

    @property
    def state(self) -> FSMContext:
        return self._state

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def by_admin(self) -> bool:
        return self._by_admin

    @property
    def by_moderator(self) -> bool:
        return self._by_moderator

    @property
    def answer(self) -> str | None:
        return self._answer

    @property
    def entries(self) -> list[Type[Entry]] | None:
        return self._entries

    @property
    def complete(self) -> str | None:
        return self._complete

    @property
    def menu(self) -> list[str] | None:
        return self._menu

    @property
    def admin_menu(self) -> list[str] | None:
        return self._admin_menu

    @property
    def moderator_menu(self) -> list[str] | None:
        return self._moderator_menu

    @property
    def role_menu(self) -> list[str] | None:
        return (
            self.admin_menu
            if self.by_admin
            else self.moderator_menu if self.by_moderator else self.menu
        )

    @property
    def results(self) -> dict[str, int | str] | None:
        return self._results

    @results.setter
    def results(self, value: dict[str, int | str] | None) -> None:
        self._results = value

    async def reply(self) -> None:
        if not self.answer:
            return
        await self.content.answer(self.answer, reply_markup=reply_keyboard(self.role_menu))

    async def process(self) -> None:
        """Process the event, which may be reimplemented in the child class to handle some specific logic."""
        if self.entries:
            stepper = Stepper(
                self.content,
                self.state,
                entries=self.entries,
                complete=self.complete,
            )
            await stepper.start()
            self._results = await stepper.get_results()


class TextEvent(BaseEvent):
    _button: str | None = None

    @classmethod
    def button(cls) -> MagicFilter:
        return F.text == cls._button


class CallbackEvent(BaseEvent):
    _callback: str | None = None
    _data_type: type | None = None

    @classmethod
    def callback(cls) -> MagicFilter:
        return F.data.startswith(cls._callback)

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
    def data(self):
        return self._data

    @property
    def answers(self) -> list[str | int] | str | int | None:
        if not self.entries:
            return None
        answers = []
        for entry in self.entries:
            answers.append(entry.get_answer(self.results))  # type: ignore[call-arg, arg-type]
        return answers if len(answers) > 1 else answers[0]
