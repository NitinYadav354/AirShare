from django.shortcuts import render, redirect
from .models import ClipboardItems
from .forms import ClipboardItemsForm
from django.utils import timezone
from datetime import timedelta
import cloudinary.uploader
from .tasks import del_clipboard_item
# Create your views here.

def submit_clipboard(request):
    code = None
    if request.method == 'POST':
        form = ClipboardItemsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            Clipboard_instance = form.save()
            delay_seconds = (Clipboard_instance.expires_at - timezone.now()).total_seconds()
            del_clipboard_item.apply_async(args=[Clipboard_instance.id], countdown=max(delay_seconds, 0))
            code = Clipboard_instance.UniqueCode

    else:
        form = ClipboardItemsForm()
        
    return render(request, 'clipboard/Clipboard.html', {'form': form, 'code': code})

def process_text(text):
    return text.replace("\t", "    ")

def fetch_clipboard(request):
    if request.method == 'POST':
        code = request.POST.get('Code')
        form = ClipboardItemsForm()
        try:
            clipboard_item = ClipboardItems.objects.get(UniqueCode=code, isfetched=False)
            clipboard_item.text = process_text(clipboard_item.text) if clipboard_item.text else clipboard_item.text
            clipboard_item.isfetched = True
            clipboard_item.save()
            del_clipboard_item.delay(clipboard_item.id)
            return render(request, 'clipboard/Clipboard.html', {'items': clipboard_item, 'form': form})
        except ClipboardItems.DoesNotExist:
            return render(request, 'clipboard/Clipboard.html', {'error': "Not found", 'form': form})
    return render(request, 'clipboard/Clipboard.html', {'form': ClipboardItemsForm()})