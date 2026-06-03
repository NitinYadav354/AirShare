from django.shortcuts import render, redirect
from .models import ClipboardItems
from .forms import ClipboardItemsForm
import cloudinary.uploader

# Create your views here.
def sumbit_clipboard(request):
    code = None
    if request.method == 'POST':
        form = ClipboardItemsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            Clipboard_instance = form.save()
            code = Clipboard_instance.UniqueCode

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
            clipboard_item.delete()
            if clipboard_item.image and clipboard_item.image.name:
                cloudinary.uploader.destroy(clipboard_item.image.name)

            if clipboard_item.documents and clipboard_item.documents.name:
                cloudinary.uploader.destroy(clipboard_item.documents.name)
            return render(request, 'clipboard/Clipboard.html', {'items': clipboard_item,'form': form})
        except ClipboardItems.DoesNotExist:
            return render(request, 'clipboard/Clipboard.html', {'error': "Not found", 'form': form})
    else:
        return render(request, 'clipboard/Clipboard.html')