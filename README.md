<div align="center" markdown>
<img src="https://github.com/iwatkot/aiogram_events/assets/118521851/8719b400-7778-4c25-94db-030d6c98c3fd">

A simple way to catch and process events in the aiogram library.

<p align="center">
    <a href="#Overview">Overview</a> •
    <a href="#Quick-Start">Quick Start</a> •
    <a href="#Core-Components">Core Components</a> •
    <a href="#Tutorial">Tutorial</a> •
    <a href="#Bugs-and-Feature-Requests">Bugs and Feature Requests</a> •
    <a href="https://pypi.org/project/aiogram_events/">PyPI</a>
</p>

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/iwatkot/aiogram_events)
![GitHub issues](https://img.shields.io/github/issues/iwatkot/aiogram_events)
[![Build Status](https://github.com/iwatkot/py3xui/actions/workflows/checks.yml/badge.svg)](https://github.com/iwatkot/aiogram_events/actions)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram_events)<br>
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram_events)
![PyPI - Version](https://img.shields.io/pypi/v/aiogram_events)
[![Maintainability](https://api.codeclimate.com/v1/badges/7eba14b75914b09a4d50/maintainability)](https://codeclimate.com/github/iwatkot/aiogram_events/maintainability)
</div>

## Overview
The `aiogram_events` library is a simple way to catch and process events in the `aiogram` library, including menus and multi-step forms. It's designed to simplify the process of creating bots and to make the code more readable and maintainable.<br>

## Quick Start
**Step 1:** Install the library.<br>
```bash
pip install aiogram_events
```
ℹ️ The library supports only `aigoram` >= 3.0.0 and Python >= 3.10.0.<br>

**Step 2:** Import library routers and add them to the bot.<br>
```python
from aiogram_events import event_router, stepper_router

dp.include_routers(event_router, stepper_router)
```
ℹ️ Order matters! The event router should be added before the stepper router in most cases.<br>

**Step 3:** Create events.<br>
For text events:
```python
from aiogram_events import TextEvent

class MainMenuEvent(TextEvent):
    _button = BUTTON_MAIN_MENU
    _answer = "Now you are in the main menu."
    _menu = [BUTTON_FORM, BUTTON_MAIN_MENU]
    _admin_menu = [BUTTON_OPTIONS, BUTTON_FORM, BUTTON_MAIN_MENU]
```

For callback events:

```python
from aiogram_events import CallbackEvent, Team
from aiogram_events.stepper import NumberEntry

class AddAdmin(CallbackEvent):
    _callback = "admin__add_admin"
    _data_type = int
    _complete = "Admin added."

    _entries = [
        NumberEntry("Telegram ID", "Incorrect user ID.", "Enter the user Telegram ID to add it.")
    ]

    async def process(self) -> None:
        await super().process(main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL, skip=BUTTON_SKIP)
        if self.answers not in Team.admins:
            Team.admins.append(self.answers)
```
Short explanation:
- `_button` - the button that will trigger the event.
- `_answer` - the message that the bot will send to the user.
- `_menu` - a list of buttons that will be displayed to the user after the message.
- `_admin_menu` - a list of buttons that will be displayed to the user if the user is an admin.
- `_callback` - the prefix for the callback that will trigger the event.
- `_data_type` - the type of data that comes with the callback.
- `_complete` - the message to be sent to the user after the form is completed.
- `_entries` - a list of `Entry` objects that will start a multi-step form.
- `process()` - a method that will be called when the event is triggered, should be reimplemented in the event class. If the event contains a form, don't forget to call the `super().process()` method to start and process the form (or reimplement this logic manually).

**Step 4:** Group events (optional).<br>
```python
from aiogram_events import TextEventGroup, CallbackEventGroup

class StartGroup(TextEventGroup):
    _events = [StartEvent, MainMenuEvent]

class AdminsCallbacksGroup(CallbackEventGroup):
    _events = [AddAdmin, RemoveAdmin]
    _prefix = "admin__"
```
Short explanation:
- `_events` - a list of events that belong to this group.
- `_prefix` - the prefix for the callbacks that will trigger the events in this group.

ℹ️ Grouping events does not change the behavior of the bot or make it faster, it's just a way to organize your code.

**Step 5:** Register events.<br>
```python
from aiogram_events.decorators import text_events, callback_events

@text_events(StartGroup)
async def start(event: TextEvent) -> None:
    await event.reply()
    await event.process()

@callback_events(AdminsCallbacksGroup)
async def admins_callbacks(event: CallbackEvent) -> None:
    await event.reply()
    await event.process()
```

ℹ️ Of course, you can add more methods to the individual events and handle them as you like. The decorators will just catch the event and pass it to the function. All other things are up to you.

**Step 6:** Check out the tutorial and read the docs.<br>
You can find a detailed tutorial in [this section](#Tutorial) and the detailed docs in the corresponding package directories.

## Core Components
You'll find detailed docs with usage examples in the corresponding package directories:
- [Decorators](aiogram_events/decorators/README.md)
- [Event](aiogram_events/event/README.md)
- [Stepper](aiogram_events/stepper/README.md)

The library is based on three main components: `Event` and `EventGroup` - which represent a single event and a group of events, `Stepper` - which is used for multi-step forms and the decorators that are used to register events.

### Event
`Event` is a base class for all events. It contains the main logic for catching and processing events. You can inherit from this class to create custom events, but it's recommended to use as a parent class one of the following classes: `TextEvent` or `CallbackEvent`. These classes are designed to work with text and callback events respectively.

#### TextEvent
These events are triggered by text messages when the text of the message matches the `_button` attribute of the event. The `TextEvent` class has the following attributes:

|     Attribute      |        Required         |                         Description                                             |
| :----------------: | :----------------------:|:------------------------------------------------------------------------------: |
|      `_button`     |           ✅            | The button that will trigger the event.                                         |
|      `_answer`     |           *️⃣            | The message that the bot will send to the user, required if `_menu` is set.     |
|       `_menu`      |           ❌            | A list of buttons that will be displayed to the user.                           |
|   `_complete`      |           *️⃣            | The message to be sent to the user after the form is completed. Required if `_entries` is set. |
|     `_entries`     |           ❌            | A list of `Entry` objects that will start a multi-step form.           |

✅ - required<br>
❌ - optional<br>
*️⃣ - required for specific conditions.<br>         

#### CallbackEvent
These events are triggered by inline buttons when the callback of the button starts with the `_callback` attribute of the event. The `CallbackEvent` class has the following attributes:

|     Attribute      |        Required         |                         Description                                             |
| :----------------: | :----------------------:|:------------------------------------------------------------------------------: |
|    `_callback`     |           ✅            | The prefix for the callback that will trigger the event.                        |
|    `_data_type`    |           ✅            | The type of data that comes with the callback.                                  |
|     `_answer`      |           *️⃣            | The message that the bot will send to the user.                                 |
|     `_menu`        |           ❌            | A list of buttons that will be displayed to the user.                           |
|   `_complete`      |           *️⃣            | The message to be sent to the user after the form is completed. Required if `_entries` is set. |
|     `_entries`     |           ❌            | A list of `Entry` objects that will start a multi-step form.           |

✅ - required<br>
❌ - optional<br>
*️⃣ - required for specific conditions.<br>


### EventGroup
To work with multiple events in one function, you can use one of the following classes: `TextEventGroup` or `CallbackEventGroup`. These classes are used to group events that are related to each other.

#### TextEventGroup
This class is used to group text events. It has the following attributes:

|     Attribute      |        Required         |                         Description                                             |
| :----------------: | :----------------------:|:------------------------------------------------------------------------------: |
|     `_events`      |           ✅            | A list of events that belong to this group.                                     |

✅ - required<br>

#### CallbackEventGroup
This class is used to group callback events. It has the following attributes:

|     Attribute      |        Required         |                         Description                                             |
| :----------------: | :----------------------:|:------------------------------------------------------------------------------: |
|     `_events`      |           ✅            | A list of events that belong to this group.                                     |
|     `_prefix`      |           ✅            | The prefix for the callbacks that will trigger the events in this group.        |

✅ - required<br><br>

ℹ️ It's important to use the same prefix for all events in the group, otherwise, the events won't be triggered correctly.

### Stepper
You don't need to work with the `Stepper` class directly, but you can use the `Entry` class to create custom entries or use the built-in entries e.g. `TextEntry` or `NumberEntry`. If you need to add some custom logic to the `Stepper` class, you can inherit from it and reimplement the required methods.

#### Entry
The library contains several built-in entries that can be used to create forms. To create a custom entry, you need to inherit from the `Entry` class, add the `base_type` attribute to it and reimplement the `validate_answer()` method. The attribute is a type to which the answer will be converted. The method should return the boolean value, `True` if the answer is correct and `False` otherwise.

### Decorators
The decorators are used to register events in the bot and to restrict access to the events by user role. The library contains the following decorators:
- `@text_event` - to register a single text event.
- `@text_events` - to register a group of text events.
- `@callback_event` - to register a single callback event.
- `@callback_events` - to register a group of callback events.
- `@admin_only` - to allow access to the event only for admin users.
- `@moderator_admin_only` - to allow access to the event only for moderator and admin users.

## Tutorial
In this step-by-step guide, you will learn how to create a simple bot from scratch using `aiogram_events`.<br>
Of course, we will start with the installation of the library. It already has the `aiogram` library as a dependency, so you don't need to install it separately. To install the library, you can use the following command:
```bash
pip install aiogram_events
```
To debug this tutorial, you'll need to obtain a bot token from the BotFather. If you don't know how to do this, you can read the official documentation [here](https://core.telegram.org/bots#6-botfather).<br>
And now let's start coding! <br><br>
**Step 1:** Import the necessary modules.<br>
```python
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from aiogram_events import (
    CallbackEvent,
    CallbackEventGroup,
    Team,
    TextEvent,
    TextEventGroup,
    event_router,
    stepper_router,
)
from aiogram_events.decorators import (
    admin_only,
    callback_events,
    text_event,
    text_events,
)
from aiogram_events.stepper import NumberEntry, TextEntry
from aiogram_events.utils import inline_keyboard
```

Let's break down the code above (just in case, for the `aiogram` modules, you can read the official documentation [here](https://docs.aiogram.dev/en/latest/)). The most important imports here are `event_router` and `stepper_router`. It's better to start with them, so you won't forget to add them to your bot. While the `event_router` is responsible for handling events and is required for the correct operation of the library, the `stepper_router` is only needed if you're creating events containing forms with multiple steps. So, if you don't need forms, you can omit the `stepper_router` import. But don't forget to add it, if you decide to add some forms later. Since the library does not have any access to the bot, it won't raise any errors if the routers aren't added to the bot, but event catching would simply not work.<br>
We will talk about other imports later when we need them. Now let's move on to the next step.<br><br>

**Step 2:** Create a bot.<br>
```python
load_dotenv("local.env")
bot_token = os.getenv("TOKEN")

dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
```
To know how to work with the `aiogram`, you can read the official documentation [here](https://docs.aiogram.dev/en/latest/). In this section, I'll only recommend using environment variables to store your bot token and for local debug you can use the `python-dotenv` library. You can install it using the following command:
```bash
pip install python-dotenv
```
And then load the environment variables from the `.env` file. In this example, I used the `local.env` file, but you can use any name you want. Just don't forget to add this file to the `.gitignore` file, so you won't accidentally push your bot token to the repository.<br>
The example structure of the `.env` file:
```env
TOKEN=your_bot_token
```

**Step 3:** Create a list of buttons (optional).<br>
```python
BUTTON_START = "/start"
BUTTON_SKIP = "⏭ Skip"
BUTTON_CANCEL = "❌ Cancel"
BUTTON_MAIN_MENU = "🏠 Main Menu"
BUTTON_OPTIONS = "⚙️ Options"
BUTTON_ADMINS = "👥 Admins"
BUTTON_FORM = "📝 Form"
```
You can store the strings for buttons in any way you like. In this example, I used constants for this purpose, but for large bots with a lot of buttons and/or for bots with multiple languages, it won't be very convenient. So it's up to you how to handle it. Friendly reminder: the `pydantic` library can be very helpful in this case. Check the official documentation [here](https://docs.pydantic.dev/latest).<br><br>
**Step 4:** Create the first simple text events.<br>
```python
class MainMenuEvent(TextEvent):
    _button = BUTTON_MAIN_MENU
    _answer = "Now you are in the main menu."
    _menu = [BUTTON_FORM, BUTTON_MAIN_MENU]
    _admin_menu = [BUTTON_OPTIONS, BUTTON_FORM, BUTTON_MAIN_MENU]


class StartEvent(MainMenuEvent):
    _button = BUTTON_START
    _answer = "Welcome to the bot!"


class StartGroup(TextEventGroup):
    _events = [StartEvent, MainMenuEvent]


@text_events(StartGroup)
async def start(event: TextEvent) -> None:
    await event.reply()
    await event.process()
```
So, what we've got here? Let's talk about it in more detail:
- `MainMenuEvent` is triggered when the user clicks the "Main Menu" button. To make this work we added the `_button` attribute with a string value of the button. The `_answer` attribute is the message that the bot will send to the user. The `_menu` attribute is a list of buttons that will be displayed to the user. The `_admin_menu` attribute is a list of buttons that will be displayed if the user is an admin. You can omit the `_admin_menu` attribute if you don't need it, all users will get the same menu then. NOTE: the `_answer` attribute is optional, if it's not set, the bot won't send any message to the user, but it's required if the `_menu` or `_admin_menu` attributes are set because Telegram sents the buttons inside of the message.
- `StartEvent` is triggered when the user sends the "/start" command. It's inherited from the `MainMenuEvent` class since in both cases we want the bot to send the same menu to the user. But you can create a separate class for this event if you need to send a different menu to the user. It's just an example of inheritance, you can use it as you like.
- `StartGroup` is a group of events that will be triggered when the user sends the "/start" command or clicks the "Main Menu" button. It's not necessary to use groups, you can handle each event individually, but it's more convenient to use groups when you have a lot of events that are related to each other. Each group class must contain the `_events` attribute with a list of events that belong to this group.
- `@text_events(StartGroup)` is a decorator that registers the `StartGroup`. It will identify the event and pass it to the decorated function. The decorator function must have the event as an argument. You can implement any needed logic in the function, but by default, all Events have the `reply()` and `process()` methods. The `reply()` method sends the message to the user, and the `process()` method is expected to be reimplemented in the event class. You can add other methods to events and handle them whatever you like. It's completely up to you, the decorator will just catch the event and pass it to the function.<br><br>

**Step 5:** Reimplement the `process()` method.<br>
The events in the previous step will work, but they won't do anything particular, we can consider them as events to navigate the user through the bot menu. But what if we want to add some logic to the event? The simplest way to do this is to reimplement the `process()` method. So let's add the event for the `Cancel` button.

```python
class CancelEvent(MainMenuEvent):
    _button = BUTTON_CANCEL
    _answer = "Operation canceled."

    async def process(self) -> None:
        await self.state.clear()


@text_event(CancelEvent)
async def cancel(event: TextEvent) -> None:
    await event.reply()
    await event.process()
```
As we did before, we inherited the `MainMenuEvent` class to send the same menu to the user. But this time we reimplemented the `process()` method. In this case, we just clear the state of the event. I won't explain here, what's the `State` and how it works, you can read about it in the detailed documentation [here](https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/index.html). But in short, when working with forms (multiple-step events), sometimes you need to clear the state and for this case, we can use a `Cancel` button. The `@text_event(CancelEvent)` decorator is the same as `@text_events(StartGroup)`, but it's used for a single event, not a group. Just keep in mind that grouping events does not change the behavior of the bot or doesn't make it faster, it's just a way to organize your code. You can group all events in one group or create a separate function for each event, it's up to you.<br><br>

**Step 6:** Use inline keyboards.
Now we're ready for something more interesting and use some inline keyboards. You can learn more about inline keyboards in the official documentation [here](https://docs.aiogram.dev/en/dev-3.x/utils/keyboard.html). In this tutorial, I assuming that you're familiar with inline keyboards and I won't explain how they work, I'll just show you how to use them with the `aiogram_events` library.

```python
Team.admins = [1234567890, 9876543210]


class OptionsEvent(TextEvent):
    _button = BUTTON_OPTIONS
    _answer = "Now you are in the options menu."
    _menu = [BUTTON_ADMINS, BUTTON_MAIN_MENU]


class AdminsEvent(TextEvent):
    _button = BUTTON_ADMINS

    async def process(self) -> None:
        reply = "Here is the list of admins. You can add or remove an admin."
        data = {
            f"Remove admin with ID: {admin}": f"{RemoveAdmin._callback}{admin}"
            for admin in Team.admins
        }
        data.update({"Add admin": AddAdmin._callback})
        await self.content.answer(reply, reply_markup=inline_keyboard(data))
```
First of all, we changed the list of admins in the `Team` class. It's not recommended to use this class in production mode, you should implement a way to store this data that meets your needs and reimplement the required functions in the `Event` class. You will find more information in the corresponding section of README.<br>
After we added a new sub-menu, but we already talked a lot about it, the important thing here is the `process()` method. In this method, we created a dictionary with the buttons and their callbacks. The key is the text of the button, and the value is the callback. So later we'll need to catch these callbacks and extract the necessary data from them. But along that way, we'll have one extra stop.<br><br>

**Step 7:** Restrict access to the event by user role.<br>
I guess it's not surprising that you need to restrict access to some events by user role. In this example, we have an event that can be accessed only by admins. Let's see how to do this.

```python
class AdminsTextGroup(TextEventGroup):
    _events = [AdminsEvent, OptionsEvent]


@text_events(AdminsTextGroup)
@admin_only
async def admins_texts(event: TextEvent) -> None:
    await event.reply()
    await event.process()
```
Not sure that there's something to explain here. You can use the `@admin_only` decorator to restrict access to the event by user role. So only admin users will be able to trigger this event. Friendly reminder: it can be convenient to group events by user role, so you can use the `@admin_only` decorator only once for the whole group, not for each event separately.<br><br>

**Step 8:** Add callback events.<br>
Ok, we're almost on a home stretch. Previously we created some inline buttons, but we didn't catch the callbacks. Let's do this now.

```python
class AddAdmin(CallbackEvent):
    _callback = "admin__add_admin"
    _data_type = int
    _complete = "Admin added."

    _entries = [
        NumberEntry("Telegram ID", "Incorrect user ID.", "Enter the user Telegram ID to add it.")
    ]

    async def process(self) -> None:
        await super().process(main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL, skip=BUTTON_SKIP)
        if self.answers not in Team.admins:
            Team.admins.append(self.answers)


class RemoveAdmin(CallbackEvent):
    _callback = "admin__remove_admin"
    _data_type = int
    _answer = "Admin removed."

    async def process(self) -> None:
        if self.data in Team.admins:
            Team.admins.remove(self.data)


class AdminsCallbacksGroup(CallbackEventGroup):
    _events = [AddAdmin, RemoveAdmin]
    _prefix = "admin__"


@callback_events(AdminsCallbacksGroup)
@admin_only
async def admins_callbacks(event: CallbackEvent) -> None:
    await event.reply()
    await event.process()
```
`CallbackEvent` works the same as `TextEvent`, but of course, it has its nuances. While the `TextEvent` has the `_button` attribute, the `CallbackEvent` has the `_callback` attribute. And the core difference is that callback will not be matched by equality but by the `.startswith()` method. This is because it's common practice to use prefixes for callbacks and add some data after the prefix. So if you're not familiar with this, here's advice: use unique prefixes for your callbacks, so you won't accidentally catch the wrong callback. Friendly reminder: if you add two events, for example, one with the prefix "info_" and another with the prefix "info_name", the second event will never be triggered, because the first event will catch all callbacks that start with "info_".<br>
The second important thing is the `_data_type` attribute. It's used to validate the data that comes with the callback. So, it's pretty simple: if you expect some integers in the callback data, you can set the `_data_type` attribute to `int` and so on.<br>
In the code example above you can also see the `_entries` attribute. We did not add it before, but it's important to mention that it can be added both in `TextEvent` and `CallbackEvent`. This list expects the `Entry` objects and will start a multi-step form if the list is not empty. You'll find detailed information about forms in the corresponding section of README. But when you add the `_entries` attribute, don't forget to add the `_complete` attribute as well. And in the process method, you should call the `super().process()` method to start and process the form. The `main_menu`, `cancel`, and `skip` arguments are optional and can be omitted. It's just a way to customize the buttons in the form.<br>
Now let's talk about the `CallbacksGroup` class. It's the same as the `TextEventGroup`, but you need to add one more attribute: the `_prefix` attribute. It's used to filter the callbacks by prefix. Ensure that all events in the group have the same prefix, otherwise, there can be some uncatchable callbacks. The `@callback_events(AdminsCallbacksGroup)` decorator is the same as `@text_events(StartGroup)`, but it's used for callback events.<br><br>

**Step 9:** Add custom form.<br>
And finally, let's add a custom form. It will be very simple, but it will show you how to work with forms in the `aiogram_events` library.<br>

```python
class FormEvent(TextEvent):
    _button = BUTTON_FORM
    _complete = "Form completed."
    _entries = [
        TextEntry("Name", "Incorrect name.", "Enter your name."),
        TextEntry("Surname", "Incorrect surname.", "Enter your surname.", skippable=True),
        NumberEntry("Age", "Incorrect age.", "Enter your age."),
    ]

    async def process(self) -> None:
        await super().process(main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL, skip=BUTTON_SKIP)

        reply = ""
        for field_name, answer in self.results.items():
            reply += f"{field_name}: {answer}\n"
        await self.content.answer(reply)


@text_event(FormEvent)
async def form(event: TextEvent) -> None:
    await event.reply()
    await event.process()
```
So, we already saw everything that contains this snippet in the previous steps. But now, we'll pay attention to working with form answers. If you will reimplement the `process()` method (and you definitely will), don't forget to call the `super().process()` method to start and process the form. After that, you can access the form answers in the `self.results` attribute. It's a dictionary where the key is the field name and the value is the answer. You can use this data as you like. In this example, we just send the answers back to the user, but you can do whatever you want with this data.<br><br>

**Step 10:** Add routers to the bot and finally run it.<br>
```python
async def main() -> None:
    dp.include_routers(event_router, stepper_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
Now our code is ready to run. One more thing I want to mention is that you must add the `event_router` and `stepper_router` to the bot, otherwise the events won't be caught. And one more very important thing: the order of the routers matters! The event will be caught by the first router that can catch it. So if you have two routers and the first one can catch the event, the second one will never catch it. So be careful with the order of the routers. Also I recommend always adding the `event_router` first and then the `stepper_router` since it will be more convenient to clear states in the `event_router` with the `Cancel` button or something like that.<br>

<details>
<summary>Full code (click to expand)</summary>

```python
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from aiogram_events import (
    CallbackEvent,
    CallbackEventGroup,
    Team,
    TextEvent,
    TextEventGroup,
    event_router,
    stepper_router,
)
from aiogram_events.decorators import (
    admin_only,
    callback_events,
    text_event,
    text_events,
)
from aiogram_events.stepper import NumberEntry, TextEntry
from aiogram_events.utils import inline_keyboard

load_dotenv("local.env")
bot_token = os.getenv("TOKEN")

dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

BUTTON_START = "/start"
BUTTON_SKIP = "⏭ Skip"
BUTTON_CANCEL = "❌ Cancel"
BUTTON_MAIN_MENU = "🏠 Main Menu"
BUTTON_OPTIONS = "⚙️ Options"
BUTTON_ADMINS = "👥 Admins"
BUTTON_FORM = "📝 Form"


class MainMenuEvent(TextEvent):
    _button = BUTTON_MAIN_MENU
    _answer = "Now you are in the main menu."
    _menu = [BUTTON_FORM, BUTTON_MAIN_MENU]
    _admin_menu = [BUTTON_OPTIONS, BUTTON_FORM, BUTTON_MAIN_MENU]


class StartEvent(MainMenuEvent):
    _button = BUTTON_START
    _answer = "Welcome to the bot!"


class StartGroup(TextEventGroup):
    _events = [StartEvent, MainMenuEvent]


@text_events(StartGroup)
async def start(event: TextEvent) -> None:
    await event.reply()
    await event.process()


class CancelEvent(MainMenuEvent):
    _button = BUTTON_CANCEL
    _answer = "Operation canceled."

    async def process(self) -> None:
        await self.state.clear()


@text_event(CancelEvent)
async def cancel(event: TextEvent) -> None:
    await event.reply()
    await event.process()


Team.admins = [1234567890, 9876543210]


class OptionsEvent(TextEvent):
    _button = BUTTON_OPTIONS
    _answer = "Now you are in the options menu."
    _menu = [BUTTON_ADMINS, BUTTON_MAIN_MENU]


class AdminsEvent(TextEvent):
    _button = BUTTON_ADMINS

    async def process(self) -> None:
        reply = "Here is the list of admins. You can add or remove an admin."
        data = {
            f"Remove admin with ID: {admin}": f"{RemoveAdmin._callback}{admin}"
            for admin in Team.admins
        }
        data.update({"Add admin": AddAdmin._callback})
        await self.content.answer(reply, reply_markup=inline_keyboard(data))


class AdminsTextGroup(TextEventGroup):
    _events = [AdminsEvent, OptionsEvent]


@text_events(AdminsTextGroup)
@admin_only
async def admins_texts(event: TextEvent) -> None:
    await event.reply()
    await event.process()


class AddAdmin(CallbackEvent):
    _callback = "admin__add_admin"
    _data_type = int
    _complete = "Admin added."

    _entries = [
        NumberEntry("Telegram ID", "Incorrect user ID.", "Enter the user Telegram ID to add it.")
    ]

    async def process(self) -> None:
        await super().process(main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL, skip=BUTTON_SKIP)
        if self.answers not in Team.admins:
            Team.admins.append(self.answers)


class RemoveAdmin(CallbackEvent):
    _callback = "admin__remove_admin"
    _data_type = int
    _answer = "Admin removed."

    async def process(self) -> None:
        if self.data in Team.admins:
            Team.admins.remove(self.data)


class AdminsCallbacksGroup(CallbackEventGroup):
    _events = [AddAdmin, RemoveAdmin]
    _prefix = "admin__"


@callback_events(AdminsCallbacksGroup)
@admin_only
async def admins_callbacks(event: CallbackEvent) -> None:
    await event.reply()
    await event.process()


class FormEvent(TextEvent):
    _button = BUTTON_FORM
    _complete = "Form completed."
    _entries = [
        TextEntry("Name", "Incorrect name.", "Enter your name."),
        TextEntry("Surname", "Incorrect surname.", "Enter your surname.", skippable=True),
        NumberEntry("Age", "Incorrect age.", "Enter your age."),
    ]

    async def process(self) -> None:
        await super().process(main_menu=BUTTON_MAIN_MENU, cancel=BUTTON_CANCEL, skip=BUTTON_SKIP)

        reply = ""
        for field_name, answer in self.results.items():
            reply += f"{field_name}: {answer}\n"
        await self.content.answer(reply)


@text_event(FormEvent)
async def form(event: TextEvent) -> None:
    await event.reply()
    await event.process()


async def main() -> None:
    dp.include_routers(event_router, stepper_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

Now, let's launch our bot and take a look at how it works.<br><br>
[![Watch the video](https://github.com/iwatkot/aiogram_events/assets/118521851/405c808d-a9c3-45d2-b0d9-23939f55e14f)](https://github.com/iwatkot/aiogram_events/assets/118521851/ff2b0fc7-9812-4463-a16e-9da483f4a4ef)

<br>

## Bugs and Feature Requests
If you find a bug or have a feature request, please open an issue on the GitHub repository.<br>
You're also welcome to contribute to the project by opening a pull request.