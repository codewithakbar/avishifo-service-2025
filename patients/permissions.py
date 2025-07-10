# permissions.py
from rest_framework.permissions import BasePermission


class IsDoctorUser(BasePermission):
    """
    Ruxsat faqat doctor user_type ga ega bo‘lgan foydalanuvchilarga beriladi
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "doctor"
