from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import ClipboardItems
from .forms import ClipboardItemsForm
from django.utils import timezone
import cloudinary.uploader
import cloudinary.utils
import time
if settings.DEBUG:
    from .tasks import del_clipboard_item


def delete_expired_items():
    expired_items = ClipboardItems.objects.filter(expires_at__lt=timezone.now())
    for item in expired_items:
        delete_clipboard_item(item)
    expired_items.delete()


def extract_public_id(url):
    if not url: return None
    try:
        parts = url.split('/upload/')
        if len(parts) > 1:
            path = parts[1]
            if path.startswith('v') and '/' in path:
                path = path.split('/', 1)[1]
            return path.rsplit('.', 1)[0]
    except Exception:
        pass
    return None

def delete_clipboard_item(item):
    image_id = extract_public_id(item.image_url)
    if image_id:
        cloudinary.uploader.destroy(image_id, resource_type='image')
    
    doc_id = extract_public_id(item.document_url)
    if doc_id:
        cloudinary.uploader.destroy(doc_id, resource_type='raw')


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

def generate_upload_signature(request):
    timestamp = int(time.time())
    
    # We are putting uploads inside the 'uploads/documents' folder
    params_to_sign = {
        'timestamp': timestamp,
        'folder': 'uploads/documents',
    }
    
    signature = cloudinary.utils.api_sign_request(
        params_to_sign,
        cloudinary.config().api_secret
    )
    
    return JsonResponse({
        'signature': signature,
        'timestamp': timestamp,
        'api_key': cloudinary.config().api_key,
        'cloud_name': cloudinary.config().cloud_name,
    })