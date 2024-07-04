"""This module contains the Stepper class, which is used to handle multi-step forms."""

import asyncio
import uuid
from typing import Any, Callable, Type

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_events.stepper.entry import Entry, FileEntry
from aiogram_events.utils.utils import get_form, reply_keyboard

router = Router()


# pylint: disable=R0902, R0913
class Stepper:
    """Represents an object, that is used to guide the user through a form with multiple steps.
    Operates with a list of Entry objects, that are used to generate a form with aiogram.
    On each step, the Stepper sends a message with the title of the current Entry.
    After the user provides an answer, the Stepper validates it and moves to the next step.
    If validation fails, the Stepper sends an error message and waits for a valid answer.
    After the last step, the Stepper saves the results and sends a completion message.

    Args:
        content (Message | CallbackQuery): The message or callback query that triggered Stepper.
        state (FSMContext): The FSMContext object that is used to store the data.
        entries (list[Entry] | None): A list of Entry objects that are used to generate the form.
        complete (str | None): A message that is sent after the last step is completed.
    """

    def __init__(
        self,
        content: Message | CallbackQuery,
        state: FSMContext,
        entries: list[Entry],
        complete: str,
        main_menu: str | None = None,
        cancel: str | None = None,
        skip: str | None = None,
    ):
        self._entries = entries
        self._complete = complete

        # Generate a unique ID for the Stepper to match aiogram handlers.
        self._id = str(uuid.uuid4())

        # Content is the message or callback query that triggered the Stepper.
        # It will be overwritten with new content when the Stepper moves forward.
        # Or in will be preserved in the case of an error,
        # when Stepper is waiting for a valid answer.
        self._content = content

        # While state is a FSMContext object, state_code is a string representation of the current
        # state which is used to match the current step of the Stepper and access the data
        # the actual state objects from the form.
        self._state = state
        self._state_code: str | None = None
        self._step = 0

        # Form is a StatesGroup object that is used to register the Stepper with aiogram.
        self._form = get_form(self.steps)

        # Buttons are used to navigate the Stepper.
        self.main_menu = main_menu or "Main Menu"
        self.cancel = cancel or "Cancel"
        self.skip = skip or "Skip"

        # Results are stored in a dictionary and are only available after the Stepper is closed.
        # Event is used to notify the results are ready.
        self._results: dict[str, str | int] | None = None
        self.results_ready = asyncio.Event()

    @property
    def id(self) -> str:
        """Returns the unique ID of the Stepper, which was generated during initialization.

        Returns:
            str: The unique ID of the Stepper.
        """
        return self._id

    @property
    def content(self) -> Message | CallbackQuery:
        """Returns the content of the Stepper, which is the message or callback query that
        triggered it.

        Returns:
            Message | CallbackQuery: The content of the Stepper.
        """
        return self._content

    @content.setter
    def content(self, value: Message | CallbackQuery) -> None:
        """Sets the content of the Stepper to a new value.

        Args:
            value (Message | CallbackQuery): The new content of the Stepper.
        """
        self._content = value

    @property
    def state(self) -> FSMContext:
        """Returns the FSMContext object of the Stepper, which is used to store the data.

        Returns:
            FSMContext: The FSMContext object of the Stepper.
        """
        return self._state

    @state.setter
    def state(self, value: FSMContext) -> None:
        """Sets the FSMContext object of the Stepper to a new value and updates the step of the
        Stepper relative to the new state.

        Args:
            value (FSMContext): The new FSMContext object of the Stepper.
        """
        self._state = value
        self._match_step()

    @property
    def entries(self) -> list[Entry]:
        """Returns the list of Entry objects of the Stepper, which are used to generate the form.

        Returns:
            list[Entry]: The list of Entry objects of the Stepper.
        """
        return self._entries

    @property
    def entry(self) -> Entry:
        """Returns the current Entry object of the Stepper.

        Returns:
            Entry: The current Entry object of the Stepper.
        """
        return self.entries[self.step]

    @property
    def previous_entry(self) -> Entry:
        """Returns the previous Entry object of the Stepper.

        Returns:
            Entry: The previous Entry object of the Stepper.
        """
        return self.entries[self.step - 1]

    @property
    def steps(self) -> list[str]:
        """Returns the list of step names of the Stepper, which are used to register the Stepper.
        Each step name is a combination of the unique ID of the Stepper and the title of the Entry.

        Returns:
            list[str]: The list of step names of the Stepper.
        """
        return [f"{self.id}{entry.title}" for entry in self.entries]

    @property
    def form(self) -> Type[StatesGroup]:
        """Returns the StatesGroup object of the Stepper, which is used to register the Stepper.

        Returns:
            StatesGroup: The StatesGroup object of the Stepper.
        """
        return self._form

    @property
    def step(self) -> int:
        """Returns the current step of the Stepper.

        Returns:
            int: The current step of the Stepper.
        """
        return self._step

    @step.setter
    def step(self, value: int) -> None:
        """Sets the current step of the Stepper to a new value.

        Args:
            value (int): The new step of the Stepper.
        """
        self._step = value

    @property
    def state_code(self) -> str | None:
        """Returns the string representation of the current state of the Stepper.

        Returns:
            str: The string representation of the current state of the Stepper or None.
        """
        return self._state_code

    @state_code.setter
    def state_code(self, value: str) -> None:
        """Sets the string representation of the current state of the Stepper to a new value.

        Args:
            value (str): The new string representation of the current state of the Stepper.
        """
        self._state_code = value

    @property
    def results(self) -> dict[str, int | str] | None:
        """Returns the results of the Stepper, which are stored in a dictionary.
        The results are only available after the Stepper is closed and the results_ready
        event is set.

        Returns:
            dict[str, str]: The results of the Stepper.
        """
        return self._results

    @results.setter
    def results(self, value: dict[str, int | str]) -> None:
        """Sets the results of the Stepper to a new value and sets the results_ready event.

        Args:
            value (dict[str, str]): The new results of the Stepper.
        """
        self._results = value
        self.results_ready.set()

    @property
    def complete(self) -> str:
        """Returns the completion message of the Stepper, which is sent after the last step
        is completed.

        Returns:
            str: The completion message of the Stepper.
        """
        return self._complete

    async def start(self) -> None:
        """Starts the Stepper and moves to the first step.

        Raises:
            ValueError: If the Stepper is already started.
        """
        if self.step == 0:
            await self._forward()
            return await self._register()

    async def _forward(self) -> None:
        """Moves the Stepper to the next step and sends the answer to the user."""
        await self.send_answer()
        await self._update_state()
        self.step += 1

    async def validate(self, content: Message | CallbackQuery) -> bool:
        """Validates the answer of the user and sends an error message if the answer is incorrect.
        For validation, the Stepper uses the validate_answer method of the previous Entry object.

        Args:
            content (Message | CallbackQuery): The message or callback query that triggered
            the Stepper.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        answer = content.text if isinstance(content, Message) else content.data
        if answer == self.skip:
            return True

        correct = await self.previous_entry.validate_answer(content)
        if not correct:
            await content.answer(self.previous_entry.incorrect)
            return False
        return True

    async def _update(self, content: Message | CallbackQuery, state: FSMContext) -> None:
        """Updates the Stepper with the new content and state.

        Args:
            content (Message | CallbackQuery): The new content of the Stepper.
            state (FSMContext): The new state of the Stepper.
        """
        self.state_code = await self.state.get_state()
        self.state = state
        self.content = content
        if not self.data:
            return

        await self.state.update_data(**self.data)

    async def close(self) -> None:
        """Closes the Stepper and saves the results."""
        await self._process_data()
        await self.content.answer(self.complete, reply_markup=reply_keyboard([self.main_menu]))
        await self.state.clear()

    async def _process_data(self) -> None:
        """Processes the data from the state and saves the results.
        Removes the unique ID of the Stepper from the keys and skips the data with the skip button.
        """
        raw_data = await self.state.get_data()
        data = {key.replace(f"{self.id}", ""): value for key, value in raw_data.items()}
        data = {key: value for key, value in data.items() if value != self.skip}
        self.results = data

    async def get_results(self) -> dict[str, int | str] | None:
        """Waits for the results to be ready and returns them.

        Returns:
            dict[str, str]: The results of the Stepper.
        """
        await self.results_ready.wait()
        return self.results

    async def _update_state(self) -> None:
        """Updates the state of the Stepper with the current step."""
        await self.state.set_state(getattr(self.form, f"{self.id}{self.entry.title}"))

    async def send_answer(self) -> None:
        """Sends the answer to the user."""
        entry = self.entry
        buttons = entry.options if entry.options else []
        if entry.skippable:
            buttons.append(self.skip)
        buttons.append(self.cancel)
        text = self._prepare_text()
        await self.content.answer(text, reply_markup=reply_keyboard(buttons))

    @property
    def ended(self) -> bool:
        """Returns True if the Stepper has ended, False otherwise.
        Uses the step and entries properties to determine if the Stepper has reached the last step.

        Returns:
            bool: True if the Stepper has ended, False otherwise.
        """
        ended = self.step == len(self.entries)
        return ended

    def _prepare_text(self) -> str:
        """Prepares the text of the message that is sent to the user using the current Entry object.

        Returns:
            str: The text of the message that is sent to the user.
        """
        entry = self.entry
        text = f"<b>{entry.title}</b>\n\n"
        if entry.description:
            text += f"{entry.description}\n"
        return text

    @property
    def _keyword(self) -> str | None:
        """Returns the keyword of the current Entry object, it's used to save the data in the state.

        Returns:
            str: The keyword of the current Entry object.
        """
        if not self.state_code:
            return None
        return self.state_code.split(":")[1]

    @property
    def _details(self) -> str | None:
        """Returns the content of the current content object.
        For Message objects, it's the text of the message, for CallbackQuery objects,
        it's the data of the query. For FileEntry objects, it's the file_id of the document,
        which can be used to download the file.

        Returns:
            str: The content of the current content object.
        """
        if isinstance(self.previous_entry, FileEntry):
            return self.content.document.file_id  # type: ignore
        if isinstance(self.content, Message):
            return self.content.text
        if isinstance(self.content, CallbackQuery):
            return self.content.data
        return None

    @property
    def data(self) -> dict[str, Any] | None:
        """Returns the pair of key-value data, where the key is the keyword of the state
        and the value is the content of the current content object.

        Returns:
            dict[str, str]: The pair of key-value data.
        """
        if not self._keyword or not self._details:
            return None
        return {self._keyword: self._details}

    def _match_step(self) -> None:
        """Updates the step of the Stepper based on the current state of the Stepper."""
        for idx, title in enumerate(self.steps):
            if self.state_code == getattr(self.form, title):
                self.step = idx + 1

    async def _register(self):
        """Registers the Stepper with aiogram and starts the form."""

        @self._form_handlers(self.steps)
        async def steps(content: Message | CallbackQuery, state: FSMContext) -> None:
            if not await self.validate(content):
                return

            await self._update(content, state)

            if self.ended:
                await self.close()
                return

            await self._forward()

    @staticmethod
    def _form_handlers(steps: list[str]) -> Callable:
        """Decorator to register the Stepper with aiogram.

        Args:
            steps (list[str]): A list of step names of the Stepper.

        Returns:
            Callable: Decorator.
        """
        attributes = [getattr(get_form(steps), step) for step in steps]

        def decorator(func: Callable) -> Callable:
            for attr in reversed(attributes):
                func = router.message(attr)(func)
            return func

        return decorator
