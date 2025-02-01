from django.db import models
import random

# Create your models here.
class ClipboardItems(models.Model):
    UniqueCode =models.CharField(max_length=4, unique=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images', blank=True, null=True )
    documents = models.FileField(upload_to='uploads/documents', blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    isfetched = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.UniqueCode:
            while True:
                code = str(random.randint(1000,9999))
                if not ClipboardItems.objects.filter(UniqueCode = code).exists():
                    self.UniqueCode = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.UniqueCode


