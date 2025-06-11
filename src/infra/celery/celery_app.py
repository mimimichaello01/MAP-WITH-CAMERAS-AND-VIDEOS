from celery import Celery

from src.settings.base import CelerySettings

celery_settings = CelerySettings()  # type: ignore

celery_app = Celery(
    #"video_tasks",
    __name__,
    broker=celery_settings.CELERY_BROKER_URL,
    backend=celery_settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(["src.infra.celery.tasks.video_tasks"])
