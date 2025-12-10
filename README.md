<div align="center">
  
  # 🤫 Whisper Telegram Bot

  <p>
    <b>A privacy-focused Telegram bot for sending "whisper" messages in groups.</b>
  </p>

  <!-- Badges -->
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python 3.11">
  </a>
  <a href="https://github.com/aiogram/aiogram">
    <img src="https://img.shields.io/badge/Aiogram-3.23-blue" alt="Aiogram">
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-15-336791" alt="PostgreSQL">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-Enabled-2496ED" alt="Docker">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  </a>

  <br><br>
  
  [Features](#-features) •
  [Installation](#-installation) •
  [Configuration](#-configuration) •
  [Tech Stack](#-tech-stack) •
  [Contributing](#-contributing)
</div>

---

## 📖 About

**Whisper Bot** allows users to send hidden messages ("whispers") in public Telegram groups. The content of the message is hidden behind a button and can only be viewed by the sender and the specified recipient.

It works primarily via **Inline Mode**, meaning you can use it in any chat without adding the bot as a member.

## ✨ Features

-   **Inline Whispers:** Type `@{bot_username} message @username` in any chat.
-   **Privacy First:** Only the sender and the target recipient can see the message text.
-   **Smart Suggestions:** The bot remembers your frequent contacts for quick access.
-   **User-Friendly Interface:**
    -   Manual username/ID entry.
    -   Select user from contacts via private chat.
-   **Internationalization (i18n):**
    -   :flag_united_states: English
    -   :flag_russia: Russian
-   **Robust Backend:** Built with asynchronous Python and PostgreSQL.

## 🚀 Installation

The easiest way to run the bot is using **Docker Compose**.

### Prerequisites
-   [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) installed.
-   A Telegram Bot Token obtained from [@BotFather](https://t.me/BotFather).

### Step-by-Step Guide

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bchudo/whisper-telegram
    cd whisper-telegram
    ```

2.  **Configure environment variables:**
    Rename `.env.example` to `.env` and populate it with your data.
    ```bash
    mv .env.example .env
    nano .env  # or use any text editor
    ```

3.  **Run with Docker:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Bot settings:**
    Make sure to enable **Inline Mode** for your bot in [@BotFather](https://t.me/BotFather) (`/mybots` -> Select Bot -> Bot Settings -> Inline Mode -> Turn on). And enable **Inline Feedback** for your bot on 100%

## ⚙️ Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `BOT_TOKEN` | Your Telegram Bot API Token | `Required` |
| `LOGGING_MODE` | Logging output (`only_file`, `only_stdout`, `all`) | `all` |
| `DEFAULT_LOCALE` | Fallback language (`en` or `ru`) | `en` |
| `DB_HOST` | Database host (use `db` for Docker) | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `whisper` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `Required` |

## 🛠 Tech Stack

-   **Language:** [Python 3.11](https://www.python.org/)
-   **Framework:** [aiogram 3.x](https://github.com/aiogram/aiogram) (Asynchronous Telegram Bot API framework)
-   **Database:** [PostgreSQL](https://www.postgresql.org/)
-   **Driver:** [asyncpg](https://github.com/MagicStack/asyncpg) (High-performance async PostgreSQL driver)
-   **I18n:** [fluent](https://projectfluent.org/) & [aiogram-i18n](https://github.com/aiogram/aiogram-i18n)
-   **Infrastructure:** Docker & Docker Compose

## 🧑‍💻 Local Development

If you want to run the bot locally without Docker:

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ensure you have a PostgreSQL database running and configure `.env` to point to `localhost`.
4.  Run the bot:
    ```bash
    python -m whisper
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/bchudo">bchudo</a>
</div>