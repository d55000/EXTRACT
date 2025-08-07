# file_handler.py
import os
import time
from pyrogram import Client
from pyrogram.types import Message
from config import config

async def download_file(client: Client, message: Message, status_message: Message) -> str:
    """
    Downloads a media file from Telegram with progress reporting.
    """
    file_path = os.path.join(config.DOWNLOAD_DIR, str(message.message_id))
    os.makedirs(file_path, exist_ok=True)
    file_path = os.path.join(file_path, getattr(message, message.media.value).file_name)

    start_time = time.time()
    async def progress(current, total):
        elapsed_time = time.time() - start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0
        await status_message.edit_text(f"Downloading... {current*100/total:.1f}% ({speed/1024/1024:.2f} MB/s)")

    await client.download_media(message, file_name=file_path, progress=progress)
    return file_path

async def upload_file(client: Client, chat_id: int, file_path: str, caption: str, status_message: Message, thumb: str = None):
    """
    Uploads a file to Telegram with progress reporting.
    """
    start_time = time.time()
    async def progress(current, total):
        elapsed_time = time.time() - start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0
        await status_message.edit_text(f"Uploading... {current*100/total:.1f}% ({speed/1024/1024:.2f} MB/s)")

    await client.send_document(chat_id, file_path, caption=caption, thumb=thumb, progress=progress)
