from django.shortcuts import render, redirect
from .models import ClipboardItems
from .forms import ClipboardItemsForm
from django.utils import timezone
from datetime import timedelta
import cloudinary.uploader

# Create your views here.

def delete_expired_items(expired_entry):
    clipboard_item = expired_entry
    if clipboard_item.image and clipboard_item.image.name:
            cloudinary.uploader.destroy(clipboard_item.image.name)

    if clipboard_item.documents and clipboard_item.documents.name:
        cloudinary.uploader.destroy(clipboard_item.documents.name)

def delete_expired():
    expiration_time = timezone.now() - timedelta(seconds=10)
    expired_entries = ClipboardItems.objects.filter(created_at__lt = expiration_time)
    for entry in expired_entries:
        delete_expired_items(entry)
    expired_entries.delete()

def submit_clipboard(request):
    code = None
    if request.method == 'POST':
        form = ClipboardItemsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            Clipboard_instance = form.save()
            code = Clipboard_instance.UniqueCode
            delete_expired()

    else:
        form = ClipboardItemsForm()
        
    return render(request, 'clipboard/Clipboard.html', {'form': form, 'code': code})

def process_text(text):
    return text.replace("\t", "    ")

def fetch_clipboard(request):
    code = request.GET.get('Code', None)
    form = ClipboardItemsForm()
    if code:
        try:
            clipboard_item  = ClipboardItems.objects.get(UniqueCode = code)
            clipboard_item.text = process_text(clipboard_item.text)
            delete_expired_items(clipboard_item)
            clipboard_item.delete()

            return render(request, 'clipboard/Clipboard.html', {'items': clipboard_item,'form': form})
        except ClipboardItems.DoesNotExist:
            return render(request, 'clipboard/Clipboard.html', {'error': "Not found", 'form': form})
    else:
        return render(request, 'clipboard/Clipboard.html')