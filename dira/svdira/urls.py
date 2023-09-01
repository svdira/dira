from django.contrib import admin
from django.urls import path, include
from asteroid import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('asteroid.urls')),  
    path('garden/',include('garden.urls')),       
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)