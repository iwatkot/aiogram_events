<a id="decorators.decorators"></a>

# decorators.decorators

This module contains decorators for event handlers.

<a id="decorators.decorators.text_event"></a>

#### text\_event

```python
def text_event(event: Type[TextEvent]) -> Callable
```

Decorator to register a handler for a single text event.
Triggered by a message from _button attribute of the event.

**Arguments**:

- `event` _Type[TextEvent]_ - Text event class.
  

**Returns**:

- `Callable` - Decorator.
  

**Examples**:

    ```python
    from aiogram_events.event import TextEvent
    from aiogram_events.decorators import text_event

    class StartEvent(TextEvent):
        _button = "/start"
        _answer = "Welcome to the bot!"
        _menu = ["Options", "Main Menu"]

    @text_event(StartEvent)
    async def start(event: TextEvent) -> None:
        await event.reply()
        await event.process()
    ```

<a id="decorators.decorators.text_events"></a>

#### text\_events

```python
def text_events(events: TextEventGroup) -> Callable
```

Decorator to register a handler for multiple text events.
Triggered by a message from _button attribute of any event.

**Arguments**:

- `events` _TextEventGroup_ - Text event group class.
  

**Returns**:

- `Callable` - Decorator.
  

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

<a id="decorators.decorators.callback_event"></a>

#### callback\_event

```python
def callback_event(callback: Type[CallbackEvent]) -> Callable
```

Decorator to register a handler for a single callback event.
Triggered if callback data starts with _callback attribute of the event.

**Arguments**:

- `callback` _Type[CallbackEvent]_ - Callback event class.
  

**Returns**:

- `Callable` - Decorator.
  

**Examples**:

    ```python
    from aiogram_events.event import CallbackEvent
    from aiogram_events.decorators import callback_event

    class StartEvent(CallbackEvent):
        _callback = "start"
        _data_type = str
        _answer = "Welcome to the bot!"

    @callback_event(StartEvent)
    async def start(event: CallbackEvent) -> None:
        await event.reply()
        await event.process()
    ```

<a id="decorators.decorators.callback_events"></a>

#### callback\_events

```python
def callback_events(callbacks: CallbackEventGroup) -> Callable
```

Decorator to register a handler for multiple callback events.
Triggered if callback data starts with _prefix attribute of the group.

**Arguments**:

- `callbacks` _CallbackEventGroup_ - Callback event group class.
  

**Returns**:

- `Callable` - Decorator.
  

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

<a id="decorators.decorators.admin_only"></a>

#### admin\_only

```python
def admin_only(func: Callable) -> Callable
```

Decorator to restrict access to admin-only commands.

**Arguments**:

- `func` _Callable_ - Function to decorate.
  

**Returns**:

- `Callable` - Decorated function.
  

**Examples**:

    ```python
    from aiogram_events.event import TextEvent
    from aiogram_events.decorators import admin_only

    SettingsEvent(TextEvent):
        _button = "Settings"
        _answer = "Settings menu."
        _menu = ["Options", "Main Menu"]

    @text_event(SettingsEvent)
    @admin_only
    async def settings(event: TextEvent) -> None:
        await event.reply()
        await event.process()
    ```

<a id="decorators.decorators.moderator_admin_only"></a>

#### moderator\_admin\_only

```python
def moderator_admin_only(func: Callable) -> Callable
```

Decorator to restrict access to commands which available for moderators and admins.

**Arguments**:

- `func` _Callable_ - Function to decorate.
  

**Returns**:

- `callable` - Decorated function.
  

**Examples**:

    ```python
    from aiogram_events.event import TextEvent
    from aiogram_events.decorators import moderator_admin_only

    SettingsEvent(TextEvent):
        _button = "Settings"
        _answer = "Settings menu."
        _menu = ["Options", "Main Menu"]

    @text_event(SettingsEvent)
    @moderator_admin_only
    async def settings(event: TextEvent) -> None:
        await event.reply()
        await event.process()
    ```

