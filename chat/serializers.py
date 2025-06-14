from rest_framework import serializers
from .models import Chat, Message
from doctors.models import Doctor
from patients.models import Patient


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    sender_avatar = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "content",
            "message_type",
            "file_url",
            "is_read",
            "created_at",
            "sender_name",
            "sender_avatar",
            "sender_type",
            "time_ago",
        ]
        read_only_fields = ["id", "created_at", "sender_type"]

    def get_sender_avatar(self, obj):
        # Возвращаем аватар отправителя
        if hasattr(obj.sender, "profile_picture") and obj.sender.profile_picture:
            return obj.sender.profile_picture.url
        return None

    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import datetime, timedelta

        now = timezone.now()
        diff = now - obj.created_at

        if diff.days > 0:
            return f"{diff.days} дн. назад"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} ч. назад"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} мин. назад"
        else:
            return "Только что"


class ChatSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.full_name", read_only=True)
    patient_name = serializers.CharField(
        source="patient.user.full_name", read_only=True
    )
    doctor_specialty = serializers.CharField(
        source="doctor.get_specialty_display", read_only=True
    )
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "doctor_name",
            "patient_name",
            "doctor_specialty",
            "last_message",
            "unread_count",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if request and request.user:
            if hasattr(request.user, "doctor_profile"):
                return obj.unread_count_for_doctor
            elif hasattr(request.user, "patient_profile"):
                return obj.unread_count_for_patient
        return 0


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["content", "message_type", "file_url"]

    def create(self, validated_data):
        chat_id = self.context["chat_id"]
        sender = self.context["request"].user

        chat = Chat.objects.get(id=chat_id)

        message = Message.objects.create(chat=chat, sender=sender, **validated_data)
        return message
