# ui.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def create_stream_selection_keyboard(streams: Dict[str, List[Dict[str, Any]]], file_id: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for selecting media streams.
    """
    buttons = []
    for stream_type, stream_list in streams.items():
        for stream in stream_list:
            label = f"{stream_type.capitalize()} {stream['index']} ({stream['codec_name']}"
            if stream_type == 'video' and stream.get('width'):
                label += f", {stream['width']}x{stream['height']}"
            if stream_type == 'audio' and stream['language'] != 'unknown':
                label += f", {stream['language']}"
            label += ")"
            buttons.append([InlineKeyboardButton(label, callback_data=f"extract_{file_id}_{stream['index']}")])

    return InlineKeyboardMarkup(buttons)

def create_format_selection_keyboard(file_id: str, stream_index: int, stream_type: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard to choose the output format for the selected stream.
    """
    buttons = [[InlineKeyboardButton("Keep Original", callback_data=f"format_{file_id}_{stream_index}_original")]]
    if stream_type == 'audio':
        buttons.append([InlineKeyboardButton("Convert to MP3", callback_data=f"format_{file_id}_{stream_index}_mp3")])
    elif stream_type == 'subtitle':
        buttons.append([InlineKeyboardButton("Convert to SRT", callback_data=f"format_{file_id}_{stream_index}_srt")])

    return InlineKeyboardMarkup(buttons)

def format_stream_info(streams: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Formats the stream information into a readable string for a message.
    """
    info_text = "📄 **Available Streams in the File:**\n"
    for stream_type, stream_list in streams.items():
        if stream_list:
            info_text += f"\n**{stream_type.capitalize()} Streams:**\n"
            for s in stream_list:
                info_text += f"  - Index: `{s['index']}`, Codec: `{s['codec_name']}`"
                if s['language'] != 'unknown':
                    info_text += f", Language: `{s['language']}`"
                info_text += "\n"
    return info_text
