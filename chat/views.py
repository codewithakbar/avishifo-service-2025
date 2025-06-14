from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, CreateMessageSerializer
from doctors.models import Doctor
from patients.models import Patient


class ChatListView(generics.ListAPIView):
    """Список чатов для текущего пользователя"""

    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Определяем тип пользователя и возвращаем соответствующие чаты
        if hasattr(user, "doctor_profile"):
            return (
                Chat.objects.filter(doctor=user.doctor_profile, is_active=True)
                .select_related("doctor__user", "patient__user")
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("-created_at")[:1]
                    )
                )
            )
        elif hasattr(user, "patient_profile"):
            return (
                Chat.objects.filter(patient=user.patient_profile, is_active=True)
                .select_related("doctor__user", "patient__user")
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("-created_at")[:1]
                    )
                )
            )
        else:
            return Chat.objects.none()


class ChatDetailView(generics.RetrieveAPIView):
    """Детали конкретного чата"""

    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return Chat.objects.filter(doctor=user.doctor_profile)
        elif hasattr(user, "patient_profile"):
            return Chat.objects.filter(patient=user.patient_profile)
        return Chat.objects.none()


class ChatMessagesView(generics.ListAPIView):
    """Сообщения в конкретном чате"""

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]
        user = self.request.user

        # Проверяем, что пользователь участник этого чата
        chat = get_object_or_404(Chat, id=chat_id)

        if hasattr(user, "doctor_profile") and chat.doctor == user.doctor_profile:
            # Отмечаем сообщения пациента как прочитанные
            Message.objects.filter(
                chat=chat, sender_type="patient", is_read=False
            ).update(is_read=True)
        elif hasattr(user, "patient_profile") and chat.patient == user.patient_profile:
            # Отмечаем сообщения врача как прочитанные
            Message.objects.filter(
                chat=chat, sender_type="doctor", is_read=False
            ).update(is_read=True)
        else:
            return Message.objects.none()

        return Message.objects.filter(chat=chat).order_by("created_at")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    """Отправка сообщения в чат"""
    try:
        chat = get_object_or_404(Chat, id=chat_id)
        user = request.user

        # Проверяем права доступа
        if hasattr(user, "doctor_profile") and chat.doctor != user.doctor_profile:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        elif hasattr(user, "patient_profile") and chat.patient != user.patient_profile:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = CreateMessageSerializer(
            data=request.data, context={"chat_id": chat_id, "request": request}
        )

        if serializer.is_valid():
            message = serializer.save()
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_or_get_chat(request):
    """Создание или получение чата между врачом и пациентом"""
    try:
        user = request.user

        if hasattr(user, "patient_profile"):
            # Пациент создает чат с врачом
            doctor_id = request.data.get("doctor_id")
            if not doctor_id:
                return Response(
                    {"error": "doctor_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            doctor = get_object_or_404(Doctor, id=doctor_id)
            patient = user.patient_profile

            chat, created = Chat.objects.get_or_create(
                doctor=doctor, patient=patient, defaults={"is_active": True}
            )

        elif hasattr(user, "doctor_profile"):
            # Врач создает чат с пациентом
            patient_id = request.data.get("patient_id")
            if not patient_id:
                return Response(
                    {"error": "patient_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            patient = get_object_or_404(Patient, id=patient_id)
            doctor = user.doctor_profile

            chat, created = Chat.objects.get_or_create(
                doctor=doctor, patient=patient, defaults={"is_active": True}
            )
        else:
            return Response(
                {"error": "User must be doctor or patient"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ChatSerializer(chat, context={"request": request})
        return Response(
            {"chat": serializer.data, "created": created},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_messages_read(request, chat_id):
    """Отметить сообщения как прочитанные"""
    try:
        chat = get_object_or_404(Chat, id=chat_id)
        user = request.user

        if hasattr(user, "doctor_profile") and chat.doctor == user.doctor_profile:
            # Врач читает сообщения пациента
            Message.objects.filter(
                chat=chat, sender_type="patient", is_read=False
            ).update(is_read=True)
        elif hasattr(user, "patient_profile") and chat.patient == user.patient_profile:
            # Пациент читает сообщения врача
            Message.objects.filter(
                chat=chat, sender_type="doctor", is_read=False
            ).update(is_read=True)
        else:
            return Response(
                {"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )

        return Response({"success": True})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
