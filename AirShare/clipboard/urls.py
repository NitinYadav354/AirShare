from django.urls import path
from .views import submit_clipboard, fetch_clipboard, generate_upload_signature
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',submit_clipboard, name = 'submit_clipboard'),
    path('fetch/', fetch_clipboard, name = 'fetch_clipboard'),
    path('api/generate-signature/', generate_upload_signature, name='generate_upload_signature'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

