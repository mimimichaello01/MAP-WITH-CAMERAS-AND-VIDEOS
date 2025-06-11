import asyncio
import os
import subprocess

async def extract_thumbnail(path: str) -> str:
    base_name = os.path.splitext(os.path.basename(path))[0]
    thumbnail_path = os.path.join(os.path.dirname(path), f"{base_name}_thumbnail.jpg")

    cmd = [
        "ffmpeg",
        "-ss", "00:00:01",
        "-i", path,
        "-vframes", "1",
        "-q:v", "2",
        "-y",
        thumbnail_path
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()
    stderr = stderr.decode('utf-8')

    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {stderr}")

    return thumbnail_path
