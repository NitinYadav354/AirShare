from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

# Create your models here.
class ClipboardItems(models.Model):
    UniqueCode =models.CharField(max_length=4, unique=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', blank=True, null=True )
    documents = models.FileField(upload_to='uploads/documents', blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    isfetched = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if not self.UniqueCode:
            while True:
                code = str(random.randint(1000,9999))
                if not ClipboardItems.objects.filter(UniqueCode = code).exists():
                    self.UniqueCode = code
                    break
        if is_new and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.UniqueCode


