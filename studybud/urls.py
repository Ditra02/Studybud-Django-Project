from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # root directory app
    path('api/', include('base.api.urls')), # any urls that start with an api or with api after the home url send them to urlspatterns inside api folder 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
