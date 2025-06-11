from fastapi import UploadFile, HTTPException, status


def validate_video_file(file: UploadFile) -> None:
    if not file.filename or not file.filename.lower().endswith(".mp4"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть в формате MP4",
        )
