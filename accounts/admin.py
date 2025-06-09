from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "user_type",
        "is_verified",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "user_type",
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "date_of_birth",
                    "address",
                    "profile_picture",
                )
            },
        ),
        ("Account info", {"fields": ("user_type", "is_verified")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "user_type",
                    "phone_number",
                ),
            },
        ),
    )

    def full_name(self, obj):
        return obj.full_name or "-"

    full_name.short_description = "Full Name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

    actions = ["verify_users", "unverify_users"]

    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} users were successfully verified.")

    verify_users.short_description = "Mark selected users as verified"

    def unverify_users(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} users were successfully unverified.")

    unverify_users.short_description = "Mark selected users as unverified"
