from types import MethodType
from typing import Callable

from aiogram.types import CallbackQuery, Message


class Entry:
    def __init__(
        self,
        title: str,
        incorrect: str,
        base_type: type,
        description: str | None = None,
        skippable: bool = False,
        options: list[str] | None = None,
        **kwargs,
    ):
        self._title = title
        self._incorrect = incorrect
        self._base_type = base_type
        self._description = description
        self._skippable = skippable
        self._options = options

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        raise NotImplementedError

    def get_answer(self, results: dict[str, int | str]) -> str | int:
        return self.base_type(results[self.title])

    def replace_validator(self, validator: Callable) -> None:
        self.validate_answer = MethodType(validator, self)  # type: ignore[method-assign]

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def incorrect(self) -> str:
        return self._incorrect

    @incorrect.setter
    def incorrect(self, value: str) -> None:
        self._incorrect = value

    @property
    def base_type(self) -> type:
        return self._base_type

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def skippable(self) -> bool:
        return self._skippable

    @skippable.setter
    def skippable(self, value: bool) -> None:
        self._skippable = value

    @property
    def options(self) -> list[str] | None:
        if self._options:
            return self._options.copy()
        return None

    @options.setter
    def options(self, value: list[str]) -> None:
        self._options = value


class TextEntry(Entry):
    base_type = str

    """Class to represent a text entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
    """

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a string.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is a string, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        try:
            assert isinstance(parsed_content, str)
            return True
        except AssertionError:
            return False
