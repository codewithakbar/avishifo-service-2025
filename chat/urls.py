from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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

# Simple health check endpoint for CORS testing
@csrf_exempt
def health_check(request):
    response = JsonResponse({"status": "ok", "message": "Chat API is working"})
    response["Access-Control-Allow-Origin"] = "https://dashboard.avishifo.uz"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

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
    path("health/", health_check, name="health-check"),  # Health check endpoint

    path('gpt/', include(router.urls)),
]
