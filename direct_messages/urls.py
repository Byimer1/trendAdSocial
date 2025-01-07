from django.urls import path
from . import views

app_name = 'direct_messages'

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('<int:conversation_id>/mark-read/', views.mark_messages_read, name='mark_messages_read'),
    path('unread-count/', views.unread_count, name='unread_count'),
] 