<a id="stepper.entry"></a>

# stepper.entry

This module contains the Entry class and most common entry types for the form stepper.

<a id="stepper.entry.Entry"></a>

## Entry Objects

```python
class Entry()
```

This is a base class for all entry types in the form stepper.

**Arguments**:

- `title` _str_ - Title of the entry
- `incorrect` _str_ - Message to display when the answer is incorrect
- `description` _str, optional_ - Description of the entry. Defaults to None.
- `skippable` _bool, optional_ - If True, the entry can be skipped. Defaults to False.
- `options` _list[str], optional_ - List of options for the entry. Defaults to None.
  

**Attributes**:

- `title` _str_ - Title of the entry
- `incorrect` _str_ - Message to display when the answer is incorrect
- `base_type` _type_ - Base type of the entry
- `description` _str_ - Description of the entry
- `skippable` _bool_ - If True, the entry can be skipped
- `options` _list[str]_ - List of options for the entry
  
  Public Methods:
- `validate_answer` - Checks if the answer is correct
- `get_answer` - Returns the answer in the correct format
  

**Examples**:

    ```python

    from aiogram_events.stepper import TextEntry

    name_entry = TextEntry(
        "Name", "Please enter a valid name", skippable=True, options=["John", "Jane"])

<a id="stepper.entry.Entry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is correct. Must be implemented in the child class.

**Arguments**:

- `content` _str_ - Answer to the entry
  

**Returns**:

- `bool` - True if the answer is correct, False otherwise

<a id="stepper.entry.Entry.get_answer"></a>

#### get\_answer

```python
def get_answer(results: dict[str, int | str]) -> str | int
```

Returns the answer in the correct format.

**Arguments**:

- `results` _dict[str, int | str]_ - Results of the form
  

**Returns**:

  str | int: Answer in the correct format

<a id="stepper.entry.Entry.title"></a>

#### title

```python
@property
def title() -> str
```

Returns the title of the entry.

**Returns**:

- `str` - Title of the entry

<a id="stepper.entry.Entry.title"></a>

#### title

```python
@title.setter
def title(value: str) -> None
```

Sets the title of the entry.

**Arguments**:

- `value` _str_ - Title of the entry

<a id="stepper.entry.Entry.incorrect"></a>

#### incorrect

```python
@property
def incorrect() -> str
```

Returns the message to display when the answer is incorrect.

**Returns**:

- `str` - Message to display when the answer is incorrect

<a id="stepper.entry.Entry.incorrect"></a>

#### incorrect

```python
@incorrect.setter
def incorrect(value: str) -> None
```

Sets the message to display when the answer is incorrect.

**Arguments**:

- `value` _str_ - Message to display when the answer is incorrect

<a id="stepper.entry.Entry.base_type"></a>

#### base\_type

```python
@property
def base_type() -> type | None
```

Returns the base type of the entry.

**Returns**:

- `type` - Base type of the entry

<a id="stepper.entry.Entry.description"></a>

#### description

```python
@property
def description() -> str | None
```

Returns the description of the entry.

**Returns**:

- `str` - Description of the entry

<a id="stepper.entry.Entry.description"></a>

#### description

```python
@description.setter
def description(value: str) -> None
```

Sets the description of the entry.

**Arguments**:

- `value` _str_ - Description of the entry

<a id="stepper.entry.Entry.skippable"></a>

#### skippable

```python
@property
def skippable() -> bool
```

Returns if the entry can be skipped.

**Returns**:

- `bool` - If True, the entry can be skipped. False otherwise.

<a id="stepper.entry.Entry.skippable"></a>

#### skippable

```python
@skippable.setter
def skippable(value: bool) -> None
```

Sets if the entry can be skipped.

**Arguments**:

- `value` _bool_ - If True, the entry can be skipped. False otherwise.

<a id="stepper.entry.Entry.options"></a>

#### options

```python
@property
def options() -> list[str] | None
```

Returns the list of options for the entry.

**Returns**:

- `list[str]` - List of options for the entry. None if no options are provided.

<a id="stepper.entry.Entry.options"></a>

#### options

```python
@options.setter
def options(value: list[str]) -> None
```

Sets the list of options for the entry.

**Arguments**:

- `value` _list[str]_ - List of options for the entry. None if no options are provided.

<a id="stepper.entry.TextEntry"></a>

## TextEntry Objects

```python
class TextEntry(Entry)
```

Class to represent a text entry in the form.

**Example**:

    ```python
    from aiogram_events.stepper import TextEntry

    name_entry = TextEntry(
        "Name", "Please enter a valid name", skippable=True, options=["John", "Jane"])
    ```

<a id="stepper.entry.TextEntry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is a string.

**Arguments**:

- `content` _Message | CallbackQuery_ - Answer to the entry.
  

**Returns**:

- `bool` - True if the answer is a string, False otherwise

<a id="stepper.entry.NumberEntry"></a>

## NumberEntry Objects

```python
class NumberEntry(Entry)
```

Class to represent a number entry in the form.

**Example**:

    ```python
    from aiogram_events.stepper import NumberEntry

    age_entry = NumberEntry(
        "Age", "Please enter a valid age", skippable=True, options=["18", "19"])
    ```

<a id="stepper.entry.NumberEntry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is a number.

**Arguments**:

- `content` _Message | CallbackQuery_ - Answer to the entry
  

**Returns**:

- `bool` - True if the answer is a number, False otherwise

<a id="stepper.entry.DateEntry"></a>

## DateEntry Objects

```python
class DateEntry(Entry)
```

Class to represent a date entry in the form.

**Example**:

    ```python
    from aiogram_events.stepper import DateEntry

    dob_entry = DateEntry(
        "Date of Birth", "Please enter a valid date", skippable=True)
    ```

<a id="stepper.entry.DateEntry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is a date.

**Arguments**:

- `content` _Message | CallbackQuery_ - Answer to the entry
  

**Returns**:

- `bool` - True if the answer is a date, False otherwise

<a id="stepper.entry.OneOfEntry"></a>

## OneOfEntry Objects

```python
class OneOfEntry(Entry)
```

Class to represent a one-of entry in the form.

**Example**:

    ```python
    from aiogram_events.stepper import OneOfEntry

    age_check_entry = OneOfEntry(
        "Age Check", "Please select one of the options", skippable=True, options=["Yes", "No"])
    ```

<a id="stepper.entry.OneOfEntry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is one of the options.

**Arguments**:

- `content` _Message | CallbackQuery_ - Answer to the entry
  

**Returns**:

- `bool` - True if the answer is one of the options, False otherwise

<a id="stepper.entry.UrlEntry"></a>

## UrlEntry Objects

```python
class UrlEntry(Entry)
```

Class to represent a url entry in the form.

**Example**:

    ```python
    from aiogram_events.stepper import UrlEntry

    website_entry = UrlEntry(
        "Website", "Please enter a valid website url", skippable=True)
    ```

<a id="stepper.entry.UrlEntry.validate_answer"></a>

#### validate\_answer

```python
async def validate_answer(content: Message | CallbackQuery) -> bool
```

Checks if the answer is a url.

**Arguments**:

- `content` _Message | CallbackQuery_ - Answer to the entry
  

**Returns**:

- `bool` - True if the answer is a url, False otherwise

<a id="stepper.stepper"></a>

# stepper.stepper

This module contains the Stepper class, which is used to handle multi-step forms.

<a id="stepper.stepper.Stepper"></a>

## Stepper Objects

```python
class Stepper()
```

Represents an object, that is used to guide the user through a form with multiple steps.
Operates with a list of Entry objects, that are used to generate a form with aiogram.
On each step, the Stepper sends a message with the title of the current Entry.
After the user provides an answer, the Stepper validates it and moves to the next step.
If validation fails, the Stepper sends an error message and waits for a valid answer.
After the last step, the Stepper saves the results and sends a completion message.

**Arguments**:

- `content` _Message | CallbackQuery_ - The message or callback query that triggered Stepper.
- `state` _FSMContext_ - The FSMContext object that is used to store the data.
- `entries` _list[Entry] | None_ - A list of Entry objects that are used to generate the form.
- `complete` _str | None_ - A message that is sent after the last step is completed.

<a id="stepper.stepper.Stepper.id"></a>

#### id

```python
@property
def id() -> str
```

Returns the unique ID of the Stepper, which was generated during initialization.

**Returns**:

- `str` - The unique ID of the Stepper.

<a id="stepper.stepper.Stepper.content"></a>

#### content

```python
@property
def content() -> Message | CallbackQuery
```

Returns the content of the Stepper, which is the message or callback query that
triggered it.

**Returns**:

  Message | CallbackQuery: The content of the Stepper.

<a id="stepper.stepper.Stepper.content"></a>

#### content

```python
@content.setter
def content(value: Message | CallbackQuery) -> None
```

Sets the content of the Stepper to a new value.

**Arguments**:

- `value` _Message | CallbackQuery_ - The new content of the Stepper.

<a id="stepper.stepper.Stepper.state"></a>

#### state

```python
@property
def state() -> FSMContext
```

Returns the FSMContext object of the Stepper, which is used to store the data.

**Returns**:

- `FSMContext` - The FSMContext object of the Stepper.

<a id="stepper.stepper.Stepper.state"></a>

#### state

```python
@state.setter
def state(value: FSMContext) -> None
```

Sets the FSMContext object of the Stepper to a new value and updates the step of the
Stepper relative to the new state.

**Arguments**:

- `value` _FSMContext_ - The new FSMContext object of the Stepper.

<a id="stepper.stepper.Stepper.entries"></a>

#### entries

```python
@property
def entries() -> list[Entry]
```

Returns the list of Entry objects of the Stepper, which are used to generate the form.

**Returns**:

- `list[Entry]` - The list of Entry objects of the Stepper.

<a id="stepper.stepper.Stepper.entry"></a>

#### entry

```python
@property
def entry() -> Entry
```

Returns the current Entry object of the Stepper.

**Returns**:

- `Entry` - The current Entry object of the Stepper.

<a id="stepper.stepper.Stepper.previous_entry"></a>

#### previous\_entry

```python
@property
def previous_entry() -> Entry
```

Returns the previous Entry object of the Stepper.

**Returns**:

- `Entry` - The previous Entry object of the Stepper.

<a id="stepper.stepper.Stepper.steps"></a>

#### steps

```python
@property
def steps() -> list[str]
```

Returns the list of step names of the Stepper, which are used to register the Stepper.
Each step name is a combination of the unique ID of the Stepper and the title of the Entry.

**Returns**:

- `list[str]` - The list of step names of the Stepper.

<a id="stepper.stepper.Stepper.form"></a>

#### form

```python
@property
def form() -> Type[StatesGroup]
```

Returns the StatesGroup object of the Stepper, which is used to register the Stepper.

**Returns**:

- `StatesGroup` - The StatesGroup object of the Stepper.

<a id="stepper.stepper.Stepper.step"></a>

#### step

```python
@property
def step() -> int
```

Returns the current step of the Stepper.

**Returns**:

- `int` - The current step of the Stepper.

<a id="stepper.stepper.Stepper.step"></a>

#### step

```python
@step.setter
def step(value: int) -> None
```

Sets the current step of the Stepper to a new value.

**Arguments**:

- `value` _int_ - The new step of the Stepper.

<a id="stepper.stepper.Stepper.state_code"></a>

#### state\_code

```python
@property
def state_code() -> str | None
```

Returns the string representation of the current state of the Stepper.

**Returns**:

- `str` - The string representation of the current state of the Stepper or None.

<a id="stepper.stepper.Stepper.state_code"></a>

#### state\_code

```python
@state_code.setter
def state_code(value: str) -> None
```

Sets the string representation of the current state of the Stepper to a new value.

**Arguments**:

- `value` _str_ - The new string representation of the current state of the Stepper.

<a id="stepper.stepper.Stepper.results"></a>

#### results

```python
@property
def results() -> dict[str, int | str] | None
```

Returns the results of the Stepper, which are stored in a dictionary.
The results are only available after the Stepper is closed and the results_ready
event is set.

**Returns**:

  dict[str, str]: The results of the Stepper.

<a id="stepper.stepper.Stepper.results"></a>

#### results

```python
@results.setter
def results(value: dict[str, int | str]) -> None
```

Sets the results of the Stepper to a new value and sets the results_ready event.

**Arguments**:

- `value` _dict[str, str]_ - The new results of the Stepper.

<a id="stepper.stepper.Stepper.complete"></a>

#### complete

```python
@property
def complete() -> str
```

Returns the completion message of the Stepper, which is sent after the last step
is completed.

**Returns**:

- `str` - The completion message of the Stepper.

<a id="stepper.stepper.Stepper.start"></a>

#### start

```python
async def start() -> None
```

Starts the Stepper and moves to the first step.

**Raises**:

- `ValueError` - If the Stepper is already started.

<a id="stepper.stepper.Stepper.validate"></a>

#### validate

```python
async def validate(content: Message | CallbackQuery) -> bool
```

Validates the answer of the user and sends an error message if the answer is incorrect.
For validation, the Stepper uses the validate_answer method of the previous Entry object.

**Arguments**:

- `content` _Message | CallbackQuery_ - The message or callback query that triggered
  the Stepper.
  

**Returns**:

- `bool` - True if the answer is correct, False otherwise.

<a id="stepper.stepper.Stepper.close"></a>

#### close

```python
async def close() -> None
```

Closes the Stepper and saves the results.

<a id="stepper.stepper.Stepper.get_results"></a>

#### get\_results

```python
async def get_results() -> dict[str, int | str] | None
```

Waits for the results to be ready and returns them.

**Returns**:

  dict[str, str]: The results of the Stepper.

<a id="stepper.stepper.Stepper.send_answer"></a>

#### send\_answer

```python
async def send_answer() -> None
```

Sends the answer to the user.

<a id="stepper.stepper.Stepper.ended"></a>

#### ended

```python
@property
def ended() -> bool
```

Returns True if the Stepper has ended, False otherwise.
Uses the step and entries properties to determine if the Stepper has reached the last step.

**Returns**:

- `bool` - True if the Stepper has ended, False otherwise.

<a id="stepper.stepper.Stepper.data"></a>

#### data

```python
@property
def data() -> dict[str, Any] | None
```

Returns the pair of key-value data, where the key is the keyword of the state
and the value is the content of the current content object.

**Returns**:

  dict[str, str]: The pair of key-value data.

