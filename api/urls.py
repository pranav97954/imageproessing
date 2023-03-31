from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload-image/', views.upload_image, name='upload-image'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
