from django.db import models
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patients.models import Patient

User = get_user_model()


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)  # Chat session title
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(
        max_length=10, choices=(("user", "User"), ("assistant", "Assistant"))
    )
    content = models.TextField()
    model_used = models.CharField(max_length=20, null=True, blank=True)  # Store which model was used
    created_at = models.DateTimeField(auto_now_add=True)


class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/")
    analyzed_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    """Модель чата между врачом и пациентом"""

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="chats")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("doctor", "patient")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Chat: Dr.{self.doctor.user.full_name} - {self.patient.user.full_name}"

    @property
    def last_message(self):
        return self.messages.first()

    @property
    def unread_count_for_patient(self):
        return self.messages.filter(sender_type="doctor", is_read=False).count()

    @property
    def unread_count_for_doctor(self):
        return self.messages.filter(sender_type="patient", is_read=False).count()


class Message1(models.Model):
    """Модель сообщения в чате"""

    SENDER_TYPES = (
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    )

    MESSAGE_TYPES = (
        ("text", "Text"),
        ("image", "Image"),
        ("file", "File"),
        ("voice", "Voice"),
    )

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPES)
    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPES, default="text"
    )
    content = models.TextField()
    file_url = models.URLField(blank=True, null=True)  # Для файлов/изображений
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}..."

    def save(self, *args, **kwargs):
        # Определяем тип отправителя
        if hasattr(self.sender, "doctor_profile"):
            self.sender_type = "doctor"
        elif hasattr(self.sender, "patient_profile"):
            self.sender_type = "patient"

        super().save(*args, **kwargs)

        # Обновляем время последнего обновления чата
        self.chat.updated_at = self.created_at
        self.chat.save(update_fields=["updated_at"])


class ChatParticipant(models.Model):
    """Участники чата (для расширения функционала)"""

    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("chat", "user")

    def __str__(self):
        return f"{self.user.full_name} in {self.chat}"
