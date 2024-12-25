# RSS Wizard Bot

RSS Wizard Bot is a Telegram bot that helps you manage RSS feeds and stay updated with your favorite news sources directly in Telegram.

## Features

- **Add RSS Feeds**: Easily add new RSS feeds.
- **View Latest Posts**: Stay updated with the latest news from your sources.
- **Easy Navigation**: Use pagination to browse entries.
- **Filter Support**: Filter posts by keywords (coming soon).
- **Delete Feeds**: Remove unnecessary RSS feeds.

## How to Run

### Requirements
- Python 3.10+
- PostgreSQL
- Docker (optional)

### Installation and Launch
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/rsswizardbot.git
   cd rsswizardbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the bot:**
   ```bash
   python bot/bot.py
   ```

## Technologies Used

- **Programming Language**: Python 3.11
- **Telegram Framework**: Aiogram 3
- **Database**: PostgreSQL (with SQLAlchemy and Alembic)
- **DI**: Dishka
- **RSS Parsing**: Feedparser
