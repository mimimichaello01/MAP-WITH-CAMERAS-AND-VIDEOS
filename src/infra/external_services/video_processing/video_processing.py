import asyncio
from src.application.dto.video import VideoMetadataDTO
import subprocess
import json
import os


async def extract_video_metadata(path: str) -> VideoMetadataDTO:
    name = os.path.basename(path)

    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-of", "json",
        path
    ]

    # Запускаем subprocess асинхронно
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe error: {stderr}")

    data = json.loads(stdout)
    stream = data["streams"][0]

    width = stream["width"]
    height = stream["height"]
    resolution = f"{width}x{height}"

    fps_str = stream["r_frame_rate"]
    num, denom = map(int, fps_str.split("/"))
    fps = round(num / denom)

    duration = int(float(stream.get("duration", 0)))

    return VideoMetadataDTO(
        name=name,
        duration=duration,
        resolution=resolution,
        fps=fps
    )
