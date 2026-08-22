import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODLUE", "Airshare.settings")

app = Celery('airshare')
app.config_from_object('django_conf:settings', namespace='CELERY')
app.autodiscover_tasks()