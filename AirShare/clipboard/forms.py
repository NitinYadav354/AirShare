from django import forms
from .models import ClipboardItems
from django.core.exceptions import ValidationError

class ClipboardItemsForm(forms.ModelForm):
    class Meta:
        model = ClipboardItems
        fields = ['text', 'image', 'documents']
        