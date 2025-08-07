# main.py
import os
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import config
from ffmpeg_utils import get_streams, extract_stream, generate_thumbnail
from ui import create_stream_selection_keyboard, format_stream_info, create_format_selection_keyboard
from file_handler import download_file, upload_file
from queue_manager import queue_manager

bot = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

user_data = {}

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("👋 Hello! Send me a media file, and I'll help you extract its streams.")

@bot.on_message(filters.media & filters.private)
async def handle_media(_, message: Message):
    status_msg = await message.reply_text("File received. Preparing to download...", quote=True)
    downloaded_path = await download_file(message._client, message, status_msg)

    await status_msg.edit_text("Analyzing media streams...")
    streams = await get_streams(downloaded_path)

    if not any(streams.values()):
        await status_msg.edit_text("Couldn't find any streams in this file.")
        shutil.rmtree(os.path.dirname(downloaded_path))
        return

    file_id = str(message.message_id)
    user_data[file_id] = {'path': downloaded_path, 'streams': streams}
    
    keyboard = create_stream_selection_keyboard(streams, file_id)
    info_text = format_stream_info(streams)
    await status_msg.edit_text(info_text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"^extract_"))
async def on_stream_select(_, query: CallbackQuery):
    await query.answer()
    file_id, stream_index_str = query.data.split("_")[1:]
    stream_index = int(stream_index_str)
    
    session = user_data.get(file_id)
    if not session:
        await query.message.edit_text("This session has expired. Please send the file again.")
        return

    stream_type = next((st for st, sl in session['streams'].items() if any(s['index'] == stream_index for s in sl)), None)
    keyboard = create_format_selection_keyboard(file_id, stream_index, stream_type)
    await query.message.edit_text("Choose the output format:", reply_markup=keyboard)

@bot.on_callback_query(filters.regex(r"^format_"))
async def on_format_select(client: Client, query: CallbackQuery):
    await query.answer()
    file_id, stream_index_str, out_format = query.data.split("_")[1:]
    
    await query.message.edit_text("Your request is in the queue and will be processed shortly.")
    await queue_manager.add_task(
        process_extraction_task, client, query, file_id, int(stream_index_str), out_format
    )

async def process_extraction_task(client: Client, query: CallbackQuery, file_id: str, stream_index: int, out_format: str):
    session = user_data.get(file_id)
    if not session: return

    status_msg = await client.send_message(query.message.chat.id, "Processing your request...")

    input_file = session['path']
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.dirname(input_file)
    ext = out_format if out_format != "original" else os.path.splitext(input_file)[1][1:]

    output_path = os.path.join(output_dir, f"{base_name}_stream_{stream_index}.{ext}")

    await status_msg.edit_text("Starting stream extraction...")
    success = await extract_stream(input_file, stream_index, output_path, None if out_format == 'original' else out_format)

    if not success:
        await status_msg.edit_text("An error occurred during extraction.")
        return
        
    thumb_path = None
    stream_type = next((st for st, sl in session['streams'].items() if any(s['index'] == stream_index for s in sl)), None)

    if stream_type == 'video':
        await status_msg.edit_text("Generating video thumbnail...")
        thumb_path = await generate_thumbnail(output_path, f"{output_path}.jpg")
    
    await upload_file(client, query.message.chat.id, output_path, f"Extracted Stream: {os.path.basename(output_path)}", status_msg, thumb_path)
    
    await status_msg.delete()

    if file_id in user_data:
        shutil.rmtree(os.path.dirname(user_data[file_id]['path']))
        if thumb_path and os.path.exists(thumb_path):
             os.remove(thumb_path)
        del user_data[file_id]

if __name__ == "__main__":
    if not os.path.exists(config.DOWNLOAD_DIR):
        os.makedirs(config.DOWNLOAD_DIR)
    print("Bot is starting...")
    bot.run()
