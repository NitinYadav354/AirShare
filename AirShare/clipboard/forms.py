from django import forms
from .models import ClipboardItems
from django.core.exceptions import ValidationError

class ClipboardItemsForm(forms.ModelForm):
    image_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    document_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    ui_image = forms.FileField(label="Image", required=False)
    ui_document = forms.FileField(label="Document", required=False)

    class Meta:
        model = ClipboardItems
        fields = ['text', 'image_url', 'document_url']
        