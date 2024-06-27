from datetime import datetime
from types import MethodType
from typing import Callable
from urllib.parse import urlparse

from aiogram.types import CallbackQuery, Message


class Entry:
    _base_type: type | None = None

    def __init__(
        self,
        title: str,
        incorrect: str,
        # base_type: type,
        description: str | None = None,
        skippable: bool = False,
        options: list[str] | None = None,
        **kwargs,
    ):
        self._title = title
        self._incorrect = incorrect
        # self._base_type = base_type
        self._description = description
        self._skippable = skippable
        self._options = options

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        raise NotImplementedError

    def get_answer(self, results: dict[str, int | str]) -> str | int:
        if self.base_type is None:
            raise ValueError("Base type not provided")
        return self.base_type(results[self.title])

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
    def base_type(self) -> type | None:
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
    """Class to represent a text entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
    """

    base_type = str

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


class NumberEntry(Entry):
    """Class to represent a number entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
    """

    base_type = int

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a number.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is a number, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        if not parsed_content:
            return False
        try:
            assert parsed_content.isdigit()
            return True
        except AssertionError:
            return False


class DateEntry(Entry):
    """Class to represent a date entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a date.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is a date, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        if not parsed_content:
            return False
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%Y.%m.%d", "%d.%m.%Y", "%m.%d.%Y"]
        for date_format in date_formats:
            try:
                datetime.strptime(parsed_content, date_format)
                return True
            except ValueError:
                continue
        return False


class OneOfEntry(Entry):
    """Class to represent a one-of entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
        options (list[str], optional): List of options for the entry. Defaults to None.
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is one of the options.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is one of the options, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        if not parsed_content:
            return False
        if not self.options:
            raise ValueError("Options not provided")
        return parsed_content in self.options


class UrlEntry(Entry):
    """Class to represent a url entry in the form.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a url.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is a url, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        try:
            check = urlparse(parsed_content)
            return all([check.scheme, check.netloc])
        except:
            return False


# class FileEntry(Entry):
#     """Class to represent a file entry in the form.

#     Args:
#         title (str): Title of the entry
#         incorrect (str): Message to display when the answer is incorrect
#         description (str, optional): Description of the entry. Defaults to None.
#     """

#     base_type = type

#     async def validate_answer(self, content: Message | CallbackQuery) -> bool:
#         """Checks if the answer is a file.

#         Args:
#             content (str): Answer to the entry

#         Returns:
#             bool: True if the answer is a file, False otherwise
#         """
#         try:
#             content = content.document.file_id
#         except AttributeError:
#             return False
#         return content is not None
