from django.shortcuts import render, redirect
from django.conf import settings
from .models import ClipboardItems
from .forms import ClipboardItemsForm
from django.utils import timezone
import cloudinary.uploader

if settings.DEBUG:
    from .tasks import del_clipboard_item


def delete_expired_items():
    expired_items = ClipboardItems.objects.filter(expires_at__lt=timezone.now())
    for item in expired_items:
        delete_clipboard_item(item)
    expired_items.delete()


def delete_clipboard_item(item):
    if item.image and item.image.name:
        cloudinary.uploader.destroy(item.image.name, resource_type='image')
    if item.documents and item.documents.name:
        cloudinary.uploader.destroy(item.documents.name, resource_type='raw')


def cleanup_expired_items():
    if not settings.DEBUG:
        delete_expired_items()


# Create your views here.

def submit_clipboard(request):
    code = None
    if request.method == 'POST':
        form = ClipboardItemsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            Clipboard_instance = form.save()
            if settings.DEBUG:
                delay_seconds = (Clipboard_instance.expires_at - timezone.now()).total_seconds()
                del_clipboard_item.apply_async(args=[Clipboard_instance.id], countdown=max(delay_seconds, 0))
            else:
                cleanup_expired_items()
            code = Clipboard_instance.UniqueCode

    else:
        form = ClipboardItemsForm()
        
    return render(request, 'clipboard/Clipboard.html', {'form': form, 'code': code})

def process_text(text):
    return text.replace("\t", "    ")

def fetch_clipboard(request):
    if request.method == 'POST':
        cleanup_expired_items()
        code = request.POST.get('Code')
        form = ClipboardItemsForm()
        try:
            clipboard_item = ClipboardItems.objects.get(UniqueCode=code, isfetched=False)
            clipboard_item.text = process_text(clipboard_item.text) if clipboard_item.text else clipboard_item.text
            clipboard_item.isfetched = True
            clipboard_item.save()
            if settings.DEBUG:
                del_clipboard_item.delay(clipboard_item.id)
            else:
                delete_clipboard_item(clipboard_item)
                clipboard_item.delete()
            return render(request, 'clipboard/Clipboard.html', {'items': clipboard_item, 'form': form})
        except ClipboardItems.DoesNotExist:
            return render(request, 'clipboard/Clipboard.html', {'error': "Not found", 'form': form})
    return render(request, 'clipboard/Clipboard.html', {'form': ClipboardItemsForm()})