from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('mcqgenerator.urls', namespace='mcqgenerator'), name='mcqgenerator'),
    path('users/', include('users.urls', namespace='users'), name='users'),
    path('blogs/', include('blogs.urls', namespace='blogs'), name='blogs'),
    path('surveys/', include('surveys.urls', namespace='surveys'), name='surveys'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
