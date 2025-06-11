from typing import Sequence
from src.application.dto.camera import CameraDTO


def camera_to_feature(camera: CameraDTO) -> dict:
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [camera.camera_longitude, camera.camera_latitude]
        },
        "properties": {
            "id": str(camera.id),
            "camera_id": camera.camera_id,
            "camera_name": camera.camera_name,
            "model": camera.model,
            "camera_place": camera.camera_place,
            "has_video": camera.has_video,
        }
    }


def cameras_to_geojson(cameras: Sequence[CameraDTO]) -> dict:
    return {
        "type": "FeatureCollection",
        "features": [camera_to_feature(camera) for camera in cameras]
    }
