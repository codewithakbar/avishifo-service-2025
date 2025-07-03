from django.urls import path, include
from .views import (
    ChatListView,
    ChatDetailView,
    ChatMessagesView,
    ChatSessionViewSet,
    UploadedImageViewSet,
    send_message,
    create_or_get_chat,
    mark_messages_read,
)

from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('chats', ChatSessionViewSet, basename='chat')
router.register('images', UploadedImageViewSet, basename='image')



urlpatterns = [
    path("", ChatListView.as_view(), name="chat-list"),
    path("create/", create_or_get_chat, name="create-chat"),
    path("<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
    path("<int:chat_id>/messages/", ChatMessagesView.as_view(), name="chat-messages"),
    path("<int:chat_id>/send/", send_message, name="send-message"),
    path("<int:chat_id>/read/", mark_messages_read, name="mark-read"),

    path('gpt/', include(router.urls)),
]
