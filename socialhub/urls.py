"""
URL configuration for socialhub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('users/', include('users.urls', namespace='users')),
    path('messages/', include('direct_messages.urls', namespace='direct_messages')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('news/', include('news.urls', namespace='news')),
    path('ads/', include('ads.urls', namespace='ads')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
