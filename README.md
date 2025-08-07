# Telegram Media Extractor Bot

A powerful Telegram bot for extracting video, audio, and subtitle streams from media files using Python, Pyrogram, and FFmpeg.

## Features

- Supports a wide range of media formats.
- Extracts video, audio, and subtitle streams.
- Interactive inline buttons for easy operation.
- Displays detailed information about each stream.
- Allows conversion to different formats (e.g., MP3 for audio).
- Handles large files with progress tracking.
- Uses a queue system to manage multiple requests.
- Automatically generates thumbnails for video streams.

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Must be installed on your system.
  - **Debian/Ubuntu**: `sudo apt update && sudo apt install ffmpeg`
  - **macOS (Homebrew)**: `brew install ffmpeg`
  - **Windows**: [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add its `bin` directory to your system's PATH.

## Getting Started

### 1. Telegram API Credentials

1.  Visit [my.telegram.org](https://my.telegram.org), log in, and go to "API development tools".
2.  Create a new application to get your `api_id` and `api_hash`.
3.  On Telegram, talk to [@BotFather](https://t.me/BotFather) to create a new bot and obtain your `BOT_TOKEN`.

### 2. Installation

1.  **Create the project directory and files** as described above.

2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

Create a `.env` file in the project's root directory and populate it with your credentials:

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
ADMINS=YOUR_TELEGRAM_USER_ID # Optional: for admin commands
DOWNLOAD_DIR=downloads/
SESSION_NAME=media_extractor_bot
