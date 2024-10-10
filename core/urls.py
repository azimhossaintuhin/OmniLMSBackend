from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import api_schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , api_schema , name="schema" ),
    path("api/v1/", include("api.v1.urls")),  # Include API URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
