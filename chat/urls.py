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
    analyze_medical_form,
    analyze_instrumental_image,
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
    path("analyze-medical-form/", analyze_medical_form, name="analyze-medical-form"),
    path("analyze-instrumental-image/", analyze_instrumental_image, name="analyze-instrumental-image"),

    path('gpt/', include(router.urls)),
    
]
