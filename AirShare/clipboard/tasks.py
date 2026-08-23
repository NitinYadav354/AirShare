from celery import shared_task
import cloudinary.uploader
from .models import ClipboardItems
from django.utils import timezone

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def del_clipboard_item(self, item_id):
    try:
        item = ClipboardItems.objects.get(id = item_id)
    except ClipboardItems.DoesNotExist:
        return

    try:
        if item.image and item.image.name:
            cloudinary.uploader.destroy(item.image.name, resource_type='image')
        if item.documents and item.documents.name:
            cloudinary.uploader.destroy(item.documents.name, resource_type='raw')
    except Exception as exc:
        raise self.retry(exc = exc)

    item.delete()

@shared_task
def sweap_expired_items():
    expired_items = ClipboardItems.objects.filter(expired_at__lt = timezone.now())
    for item in expired_items:
        del_clipboard_item.delay(item.id)


