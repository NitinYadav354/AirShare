from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ClipboardItems

@shared_task
def delete_expired():
    expiration_time = timezone.now() - timedelta(seconds=10)
    expired_entries = ClipboardItems.objects.filter(created_at__lt = expiration_time)
    expired_entries.delete()