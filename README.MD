## Telegram Bot Template v3

Telegram Bot Template v3 is a customizable template for creating Telegram Bots using Python and aiogram 3.X library. It provides a simple structure and basic functionality to kickstart your Telegram Bot development process.

## Features

- Integration with a PostgreSQL database for storing and retrieving data via SQLAlchemy ORM.
- Custom HTTP client for making requests to external APIs.
- Clear separation of concerns with distinct data and domain layers.
- Implementation of basic features of the aiogram 3.0 library.
- Implementation of basic localization feature
- Custom classes like broadcaster for additional functionality.

## Getting Started

Follow these steps to set up your Telegram bot using this template:
1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a new Telegram Bot using [BotFather](https://core.telegram.org/bots#6-botfather).
4. Copy your bot's token provided by BotFather.
5. Replace the `TOKEN` variable in `.env` with your Bot's token.
6. Customize the Bot's behavior and add your own functionality in the `bot.py` file.
7. Run `bot.py` to start your Bot: `python bot.py`.

## Usage

The `bot.py` file contains the main code for your Telegram Bot. You can customize this file to add new commands, message handlers, or any other functionality your Bot requires.

Here's an example of handling text messages using the aiogram library:

```python
@some_router.message()
async def handle_text(message: types.Message):
    await message.answer("Hello! You said: " + message.text)
