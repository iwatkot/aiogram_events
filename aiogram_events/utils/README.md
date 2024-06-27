<a id="utils.utils"></a>

# utils.utils

This module contains utility functions and classes that are used in aiogram.

<a id="utils.utils.inline_keyboard"></a>

#### inline\_keyboard

```python
def inline_keyboard(
        data: dict[str, str] | None = None) -> InlineKeyboardMarkup | None
```

Returns an InlineKeyboardMarkup object with buttons.

**Arguments**:

- `data` _dict[str, str]_ - Dictionary of buttons, where the key is the text and the value is
  the data
  

**Returns**:

- `InlineKeyboardMarkup` - InlineKeyboardMarkup object with buttons or None if
  no buttons are provided.

<a id="utils.utils.reply_keyboard"></a>

#### reply\_keyboard

```python
def reply_keyboard(
        buttons: list[str] | None = None) -> ReplyKeyboardMarkup | None
```

Returns a ReplyKeyboardMarkup object with buttons.

**Arguments**:

- `buttons` _list[str]_ - List of buttons
  

**Returns**:

- `ReplyKeyboardMarkup` - ReplyKeyboardMarkup object with buttons or None
  if no buttons are provided.

<a id="utils.utils.buttons_per_row"></a>

#### buttons\_per\_row

```python
def buttons_per_row(buttons: int) -> int
```

Returns the number of buttons per row based on the number of buttons.

**Arguments**:

- `buttons` _int_ - Number of buttons
  

**Returns**:

- `int` - Number of buttons per row

<a id="utils.utils.FormMeta"></a>

## FormMeta Objects

```python
class FormMeta(type)
```

Simple class to set attributes as State objects without creating
the instance of the class.

<a id="utils.utils.CombinedMeta"></a>

## CombinedMeta Objects

```python
class CombinedMeta(FormMeta, type(StatesGroup))
```

Since the StatesGroup already has it's metaclass, we need to combine it
with our metaclass.

<a id="utils.utils.get_form"></a>

#### get\_form

```python
def get_form(steps: list[str]) -> Type[StatesGroup]
```

Returns a new class, with attributes as State objects.

**Arguments**:

- `steps` _list[str]_ - List of steps
  

**Returns**:

- `StatesGroup` - New class with steps as State objects

