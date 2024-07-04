"""This module contains the Entry class and most common entry types for the form stepper."""

from datetime import datetime
from urllib.parse import urlparse

from aiogram.types import CallbackQuery, Message


class Entry:
    """This is a base class for all entry types in the form stepper.

    Args:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        description (str, optional): Description of the entry. Defaults to None.
        skippable (bool, optional): If True, the entry can be skipped. Defaults to False.
        options (list[str], optional): List of options for the entry. Defaults to None.

    Attributes:
        title (str): Title of the entry
        incorrect (str): Message to display when the answer is incorrect
        base_type (type): Base type of the entry
        description (str): Description of the entry
        skippable (bool): If True, the entry can be skipped
        options (list[str]): List of options for the entry

    Public Methods:
        validate_answer: Checks if the answer is correct
        get_answer: Returns the answer in the correct format

    Examples:
        ```python

        from aiogram_events.stepper import TextEntry

        name_entry = TextEntry(
            "Name", "Please enter a valid name", skippable=True, options=["John", "Jane"])
    """

    _base_type: type | None = None

    # pylint: disable=R0913
    def __init__(
        self,
        title: str,
        incorrect: str,
        description: str | None = None,
        skippable: bool = False,
        options: list[str] | None = None,
    ):
        self._title = title
        self._incorrect = incorrect
        self._description = description
        self._skippable = skippable
        self._options = options

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is correct. Must be implemented in the child class.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is correct, False otherwise"""
        raise NotImplementedError

    def get_answer(self, results: dict[str, int | str]) -> str | int:
        """Returns the answer in the correct format.

        Args:
            results (dict[str, int | str]): Results of the form

        Returns:
            str | int: Answer in the correct format"""
        if self.base_type is None:
            raise ValueError("Base type not provided")
        return self.base_type(results[self.title])  # pylint: disable=E1102

    @property
    def title(self) -> str:
        """Returns the title of the entry.

        Returns:
            str: Title of the entry"""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Sets the title of the entry.

        Args:
            value (str): Title of the entry"""
        self._title = value

    @property
    def incorrect(self) -> str:
        """Returns the message to display when the answer is incorrect.

        Returns:
            str: Message to display when the answer is incorrect"""
        return self._incorrect

    @incorrect.setter
    def incorrect(self, value: str) -> None:
        """Sets the message to display when the answer is incorrect.

        Args:
            value (str): Message to display when the answer is incorrect"""
        self._incorrect = value

    @property
    def base_type(self) -> type | None:
        """Returns the base type of the entry.

        Returns:
            type: Base type of the entry"""
        return self._base_type

    @property
    def description(self) -> str | None:
        """Returns the description of the entry.

        Returns:
            str: Description of the entry"""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the description of the entry.

        Args:
            value (str): Description of the entry"""
        self._description = value

    @property
    def skippable(self) -> bool:
        """Returns if the entry can be skipped.

        Returns:
            bool: If True, the entry can be skipped. False otherwise."""
        return self._skippable

    @skippable.setter
    def skippable(self, value: bool) -> None:
        """Sets if the entry can be skipped.

        Args:
            value (bool): If True, the entry can be skipped. False otherwise."""
        self._skippable = value

    @property
    def options(self) -> list[str] | None:
        """Returns the list of options for the entry.

        Returns:
            list[str]: List of options for the entry. None if no options are provided."""
        if self._options:
            return self._options.copy()
        return None

    @options.setter
    def options(self, value: list[str]) -> None:
        """Sets the list of options for the entry.

        Args:
            value (list[str]): List of options for the entry. None if no options are provided."""
        self._options = value


class TextEntry(Entry):
    """Class to represent a text entry in the form.

    Example:
        ```python
        from aiogram_events.stepper import TextEntry

        name_entry = TextEntry(
            "Name", "Please enter a valid name", skippable=True, options=["John", "Jane"])
        ```
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a string.

        Args:
            content (Message | CallbackQuery): Answer to the entry.

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

    Example:
        ```python
        from aiogram_events.stepper import NumberEntry

        age_entry = NumberEntry(
            "Age", "Please enter a valid age", skippable=True, options=["18", "19"])
        ```
    """

    base_type = int

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a number.

        Args:
            content (Message | CallbackQuery): Answer to the entry

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

    Example:
        ```python
        from aiogram_events.stepper import DateEntry

        dob_entry = DateEntry(
            "Date of Birth", "Please enter a valid date", skippable=True)
        ```
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a date.

        Args:
            content (Message | CallbackQuery): Answer to the entry

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

    Example:
        ```python
        from aiogram_events.stepper import OneOfEntry

        age_check_entry = OneOfEntry(
            "Age Check", "Please select one of the options", skippable=True, options=["Yes", "No"])
        ```
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is one of the options.

        Args:
            content (Message | CallbackQuery): Answer to the entry

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

    Example:
        ```python
        from aiogram_events.stepper import UrlEntry

        website_entry = UrlEntry(
            "Website", "Please enter a valid website url", skippable=True)
        ```
    """

    base_type = str

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a url.

        Args:
            content (Message | CallbackQuery): Answer to the entry

        Returns:
            bool: True if the answer is a url, False otherwise
        """
        parsed_content = content.text if isinstance(content, Message) else content.data
        try:
            check = urlparse(parsed_content)
            return all([check.scheme, check.netloc])
        except Exception:  # pylint: disable=W0718
            return False


class FileEntry(Entry):
    """Class to represent a file entry in the form.

    Example:
        ```python
        from aiogram_events.stepper import FileEntry

        resume_entry = FileEntry(
            "Resume", "Please upload a valid resume", skippable=True)
        ```
    """

    base_type = type

    async def validate_answer(self, content: Message | CallbackQuery) -> bool:
        """Checks if the answer is a file.

        Args:
            content (str): Answer to the entry

        Returns:
            bool: True if the answer is a file, False otherwise
        """
        try:
            content = content.document.file_id  # type: ignore
        except AttributeError:
            return False
        return content is not None
