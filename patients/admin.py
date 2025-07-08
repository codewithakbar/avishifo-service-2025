from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, PatientVaqtincha



admin.site.register(PatientVaqtincha)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "get_full_name",
        "get_email",
        "blood_type",
        "get_phone_number",
        "emergency_contact_name",
        "created_at",
    )
    list_filter = (
        "blood_type",
        "created_at",
        "updated_at",
        "user__is_verified",
        "user__is_active",
    )
    search_fields = (
        "patient_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone_number",
        "emergency_contact_name",
        "emergency_contact_phone",
    )
    readonly_fields = ("patient_id", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Patient Information", {"fields": ("patient_id", "user", "blood_type")}),
        (
            "Emergency Contact",
            {"fields": ("emergency_contact_name", "emergency_contact_phone")},
        ),
        (
            "Medical Information",
            {"fields": ("medical_history", "allergies", "current_medications")},
        ),
        ("Insurance", {"fields": ("insurance_number",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_full_name(self, obj):
        return obj.user.full_name

    get_full_name.short_description = "Full Name"
    get_full_name.admin_order_field = "user__first_name"

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

    def get_phone_number(self, obj):
        return obj.user.phone_number or "-"

    get_phone_number.short_description = "Phone"
    get_phone_number.admin_order_field = "user__phone_number"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    autocomplete_fields = ["user"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Patient._meta.get_field(
                "user"
            ).related_model.objects.filter(user_type="patient")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
