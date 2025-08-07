# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the bot.
    Reads settings from environment variables.
    """
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "").split(",") if admin]
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "downloads/")
    SESSION_NAME = os.environ.get("SESSION_NAME", "media_extractor_bot")

config = Config()
