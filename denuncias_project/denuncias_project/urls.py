from django.contrib import admin
from django.urls import path, include
from denuncias.views import HomeView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('denuncias/', include('denuncias.urls')),
    path('login/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home'),
]


# Servir archivos cargados solo durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)