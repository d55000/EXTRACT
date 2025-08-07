# ffmpeg_utils.py
import ffmpeg
import os
from typing import List, Dict, Any, Optional

async def probe_media(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Probes a media file to get its stream information using ffprobe.
    """
    try:
        return ffmpeg.probe(file_path)
    except ffmpeg.Error as e:
        print(f"FFprobe Error: {e.stderr.decode()}")
        return None

async def get_streams(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extracts and organizes stream information from a media file.
    """
    probe = await probe_media(file_path)
    if not probe:
        return {}

    streams = {'video': [], 'audio': [], 'subtitle': []}
    for stream in probe.get('streams', []):
        stream_type = stream.get('codec_type')
        info = {
            'index': stream.get('index'),
            'codec_name': stream.get('codec_name', 'N/A'),
            'language': stream.get('tags', {}).get('language', 'unknown'),
            'bit_rate': stream.get('bit_rate'),
            'width': stream.get('width'),
            'height': stream.get('height'),
        }
        if stream_type in streams:
            streams[stream_type].append(info)
    return streams

async def extract_stream(input_file: str, stream_index: int, output_path: str, output_format: Optional[str] = None) -> bool:
    """
    Extracts a specific stream from a media file using FFmpeg.
    """
    try:
        input_stream = ffmpeg.input(input_file)
        output_stream = input_stream[str(stream_index)]

        args = {'c': 'copy'} if not output_format else {'f': output_format}

        (
            ffmpeg.output(output_stream, output_path, **args)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg Extraction Error: {e.stderr.decode()}")
        return False

async def generate_thumbnail(video_path: str, thumb_path: str) -> Optional[str]:
    """
    Generates a thumbnail from a video file.
    """
    try:
        (
            ffmpeg.input(video_path, ss=5) # Capture frame at 5 seconds
            .output(thumb_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return thumb_path
    except ffmpeg.Error as e:
        print(f"Thumbnail Generation Error: {e.stderr.decode()}")
        return None
