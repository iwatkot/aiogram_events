<a id="event.event"></a>

# event.event

This module contains the base classes for single text and callback events.

<a id="event.event.Team"></a>

## Team Objects

```python
class Team()
```

This is a simple class to store the user IDs of the admins and moderators.
It's recommended to change the way of storing the user IDs based on the project requirements.
And reimplement the is_admin and is_moderator methods in the child class of BaseEvent.
But still, you can use this class as is.
NOTE: This class won't somehow back up the user IDs, so if the bot restarts,
the user IDs will be lost. Therefore, it's not recommended to use this class in production.

**Example**:

    ```python
    from aiogram_events.event import Team

    Team.admins = [123456789]
    Team.moderators = [987654321]
    ```

<a id="event.event.BaseEvent"></a>

## BaseEvent Objects

```python
class BaseEvent()
```

This is a base class for single text and callback events.

**Arguments**:

- `content` _Message | CallbackQuery_ - The content of the event.
- `state` _FSMContext_ - The state of the event.
  

**Attributes**:

- `content` _Message | CallbackQuery_ - The content of the event.
- `state` _FSMContext_ - The state of the event.
- `user_id` _int_ - The user ID of the event.
- `by_admin` _bool_ - True if the event is triggered by an admin, False otherwise.
- `by_moderator` _bool_ - True if the event is triggered by a moderator, False otherwise.
- `answer` _str | None_ - The answer to the event.
- `entries` _list[Entry] | None_ - The entries of the event.
- `complete` _str | None_ - Message which will be sent when entries are completed.
- `menu` _list[str] | None_ - The list of menu buttons of the event.
- `admin_menu` _list[str] | None_ - The list of admin menu buttons of the event.
- `moderator_menu` _list[str] | None_ - The list of moderator menu buttons of the event.
- `results` _dict[str, int | str] | None_ - The results of the event, where keys
  are the names of the entries and values are the answers.
  
  Public Methods:
- `is_admin(user_id` - int) -> bool: Check if the user is an admin.
- `is_moderator(user_id` - int) -> bool: Check if the user is a moderator.
  reply() -> None: Reply to the event.
  process(**kwargs) -> None: Process the event. Can be reimplemented in the child class.
  Or can be extended with additional logic by using super().process() in the child class.
  If the event has entries, it will start the stepper to process the entries.
  Through the **kwargs parameter, you can pass additional arguments to the stepper.
  Such as main_menu, cancel, and skip which are buttons for the stepper.

<a id="event.event.BaseEvent.is_admin"></a>

#### is\_admin

```python
def is_admin(user_id: int) -> bool
```

Check if the user is an admin.
It's recommended to reimplement this method in the child class.

**Arguments**:

- `user_id` _int_ - The user ID to check.
  

**Returns**:

- `bool` - True if the user is an admin, False otherwise.

<a id="event.event.BaseEvent.is_moderator"></a>

#### is\_moderator

```python
def is_moderator(user_id: int) -> bool
```

Check if the user is a moderator.
It's recommended to reimplement this method in the child class.

**Arguments**:

- `user_id` _int_ - The user ID to check.
  

**Returns**:

- `bool` - True if the user is a moderator, False otherwise.

<a id="event.event.BaseEvent.content"></a>

#### content

```python
@property
def content() -> Message | CallbackQuery
```

Returns the content of the event.

**Returns**:

  Message | CallbackQuery: The content of the event.

<a id="event.event.BaseEvent.state"></a>

#### state

```python
@property
def state() -> FSMContext
```

Returns the state of the event.

**Returns**:

- `FSMContext` - The state of the event.

<a id="event.event.BaseEvent.user_id"></a>

#### user\_id

```python
@property
def user_id() -> int
```

Returns the user ID of the event.

**Returns**:

- `int` - The user ID of the event.

<a id="event.event.BaseEvent.by_admin"></a>

#### by\_admin

```python
@property
def by_admin() -> bool
```

Returns True if the event is triggered by an admin, False otherwise.

**Returns**:

- `bool` - True if the event is triggered by an admin, False otherwise.

<a id="event.event.BaseEvent.by_moderator"></a>

#### by\_moderator

```python
@property
def by_moderator() -> bool
```

Returns True if the event is triggered by a moderator, False otherwise.

**Returns**:

- `bool` - True if the event is triggered by a moderator, False otherwise.

<a id="event.event.BaseEvent.answer"></a>

#### answer

```python
@property
def answer() -> str | None
```

Returns the answer to the event.

**Returns**:

  str | None: The answer to the event.

<a id="event.event.BaseEvent.entries"></a>

#### entries

```python
@property
def entries() -> list[Entry] | None
```

Returns the entries of the event.

**Returns**:

  list[Entry] | None: The entries of the event.

<a id="event.event.BaseEvent.complete"></a>

#### complete

```python
@property
def complete() -> str | None
```

Returns a message which will be sent when entries are completed.

**Returns**:

  str | None: The complete step of the event.

<a id="event.event.BaseEvent.menu"></a>

#### menu

```python
@property
def menu() -> list[str] | None
```

Returns the list of menu buttons of the event.

**Returns**:

  list[str] | None: The list of menu buttons of the event.

<a id="event.event.BaseEvent.admin_menu"></a>

#### admin\_menu

```python
@property
def admin_menu() -> list[str] | None
```

Returns the list of admin menu buttons of the event.

**Returns**:

  list[str] | None: The list of admin menu buttons of the event.

<a id="event.event.BaseEvent.moderator_menu"></a>

#### moderator\_menu

```python
@property
def moderator_menu() -> list[str] | None
```

Returns the list of moderator menu buttons of the event.

**Returns**:

  list[str] | None: The list of moderator menu buttons of the event.

<a id="event.event.BaseEvent.role_menu"></a>

#### role\_menu

```python
@property
def role_menu() -> list[str] | None
```

Returns the menu buttons based on the user role.

**Returns**:

  list[str] | None: The list of menu buttons based on the user role.

<a id="event.event.BaseEvent.results"></a>

#### results

```python
@property
def results() -> dict[str, int | str] | None
```

Returns the results of the event, where keys are the names of the entries and
values are the answers.

**Returns**:

  dict[str, int | str] | None: The results of the event.

<a id="event.event.BaseEvent.results"></a>

#### results

```python
@results.setter
def results(value: dict[str, int | str] | None) -> None
```

Sets the results of the event.

**Arguments**:

- `value` _dict[str, int | str] | None_ - The results of the event.

<a id="event.event.BaseEvent.reply"></a>

#### reply

```python
async def reply() -> None
```

If the answer is set, reply to the event with the answer and the menu buttons.

<a id="event.event.BaseEvent.process"></a>

#### process

```python
async def process(**kwargs) -> None
```

Process the event. Can be reimplemented in the child class.
If working with entries, it's recommended to extend this method in the child class
and use super().process() to add additional logic.

**Example**:

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
                        reply += f"{field_name}: {answer}
"
                    await self.content.answer(reply)
        ```

<a id="event.event.TextEvent"></a>

## TextEvent Objects

```python
class TextEvent(BaseEvent)
```

This is a base class for single text events.
Each text event should have a _button attribute which is a string to filter the event.
To answer the event, set the _answer attribute, if needed to update the menu
buttons set the _menu attribute.
NOTE: _answer property is required if _menu is set, since the Telegram API sents
the menu buttons inside of the message. If the _answer is not set, the menu
will not be displayed/updated.

**Example**:

    ```python
    from aiogram_events.event import TextEvent

    class OptionsEvent(TextEvent):
        _button = BUTTON_OPTIONS
        _answer = "Options selected."
        _menu = [BUTTON_OPTION_1, BUTTON_OPTION_2, BUTTON_OPTION_3]

        async def process(self) -> None:
            await super().process()
    ```

<a id="event.event.TextEvent.button"></a>

#### button

```python
@classmethod
def button(cls) -> MagicFilter
```

Returns a MagicFilter to filter the event by the button.

**Returns**:

- `MagicFilter` - The MagicFilter to filter the event by the button.

<a id="event.event.CallbackEvent"></a>

## CallbackEvent Objects

```python
class CallbackEvent(BaseEvent)
```

This is a base class for single callback events.
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

**Example**:

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

<a id="event.event.CallbackEvent.callback"></a>

#### callback

```python
@classmethod
def callback(cls) -> MagicFilter
```

Returns a MagicFilter to filter the event by the callback.

**Returns**:

- `MagicFilter` - The MagicFilter to filter the event by the callback.

<a id="event.event.CallbackEvent.data"></a>

#### data

```python
@property
def data() -> Any | None
```

Returns the data of the event.

**Returns**:

  Any | None: The data of the event.

<a id="event.event.CallbackEvent.answers"></a>

#### answers

```python
@property
def answers() -> list[str | int] | str | int | None
```

Returns the answers of the event.
If list of entries contains only one entry, it will return the answer as a single value.
Otherwise, it will return the answers as a list.
In both cases, it only returns the answers of the entries, without the names.
To get the answers with the names, use the results property.

**Returns**:

  list[str | int] | str | int | None: The answers of the event.

<a id="event.event_group"></a>

# event.event\_group

This module contains base classes for grouping text and callback events.

<a id="event.event_group.TextEventGroup"></a>

## TextEventGroup Objects

```python
class TextEventGroup()
```

This is a base class for grouping text events, should be used with text_events decorator.
Each group should have a _events attribute with a list of text events.

**Examples**:

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

<a id="event.event_group.TextEventGroup.events"></a>

#### events

```python
@property
def events() -> list[Type[TextEvent]] | None
```

Returns a list of text events or None.

**Returns**:

  list[Type[TextEvent]] | None: List of text events or None.

<a id="event.event_group.TextEventGroup.buttons"></a>

#### buttons

```python
@classmethod
def buttons(cls) -> MagicFilter
```

Returns a MagicFilter object to register a handler for multiple text events.

**Returns**:

- `MagicFilter` - MagicFilter object.

<a id="event.event_group.TextEventGroup.event"></a>

#### event

```python
@classmethod
def event(cls, message: Message, state: FSMContext) -> TextEvent | None
```

Finds a text event in the group by the message text.

**Arguments**:

- `message` _Message_ - Message object.
- `state` _FSMContext_ - FSMContext object.
  

**Returns**:

  TextEvent | None: Text event or None.

<a id="event.event_group.CallbackEventGroup"></a>

## CallbackEventGroup Objects

```python
class CallbackEventGroup()
```

This is a base class for grouping callback events, should be used with
callback_event decorator.

**Examples**:

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

<a id="event.event_group.CallbackEventGroup.events"></a>

#### events

```python
@property
def events() -> list[Type[CallbackEvent]] | None
```

Returns a list of callback events or None.

**Returns**:

  list[Type[CallbackEvent]] | None: List of callback events or None.

<a id="event.event_group.CallbackEventGroup.prefix"></a>

#### prefix

```python
@property
def prefix() -> str | None
```

Returns a prefix for the group or None.

**Returns**:

  str | None: Prefix for the group or None.

<a id="event.event_group.CallbackEventGroup.callbacks"></a>

#### callbacks

```python
@classmethod
def callbacks(cls) -> MagicFilter
```

Returns a MagicFilter object to register a handler for multiple callback events.

**Returns**:

- `MagicFilter` - MagicFilter object.

<a id="event.event_group.CallbackEventGroup.callback"></a>

#### callback

```python
@classmethod
def callback(cls, query: CallbackQuery,
             state: FSMContext) -> CallbackEvent | None
```

Finds a callback event in the group by the query data.

**Arguments**:

- `query` _CallbackQuery_ - CallbackQuery object.
- `state` _FSMContext_ - FSMContext object.
  

**Returns**:

  CallbackEvent | None: Callback event or None.

