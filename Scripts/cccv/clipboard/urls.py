from django.urls import path
from .views import sumbit_clipboard, fetch_clipboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',sumbit_clipboard, name = 'submit_clipboard'),
    path('fetch/', fetch_clipboard, name = 'fetch_clipboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

