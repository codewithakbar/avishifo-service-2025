from django.contrib import admin
from django.utils.html import format_html
from .models import MedicalRecord, MedicalRecordAttachment


class MedicalRecordAttachmentInline(admin.TabularInline):
    model = MedicalRecordAttachment
    extra = 0
    fields = ("file", "attachment_type", "description")
    readonly_fields = ("uploaded_at",)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "get_patient_name",
        "get_doctor_name",
        "diagnosis",
        "get_appointment_date",
        "follow_up_required",
        "created_at",
    )
    list_filter = (
        "follow_up_required",
        "doctor__specialty",
        "doctor__hospital",
        "created_at",
        "follow_up_date",
    )
    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "patient__patient_id",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "diagnosis",
        "chief_complaint",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    inlines = [MedicalRecordAttachmentInline]

    fieldsets = (
        (
            "Patient & Doctor Information",
            {"fields": ("patient", "doctor", "appointment")},
        ),
        (
            "Medical History",
            {
                "fields": (
                    "chief_complaint",
                    "history_of_present_illness",
                    "physical_examination",
                )
            },
        ),
        (
            "Diagnosis & Treatment",
            {"fields": ("diagnosis", "treatment", "prescription")},
        ),
        (
            "Vital Signs",
            {
                "fields": (
                    "blood_pressure",
                    "heart_rate",
                    "temperature",
                    "respiratory_rate",
                    "oxygen_saturation",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Follow-up", {"fields": ("follow_up_required", "follow_up_date", "notes")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_patient_name(self, obj):
        return obj.patient.user.full_name

    get_patient_name.short_description = "Patient"
    get_patient_name.admin_order_field = "patient__user__first_name"

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.full_name}"

    get_doctor_name.short_description = "Doctor"
    get_doctor_name.admin_order_field = "doctor__user__first_name"

    def get_appointment_date(self, obj):
        if obj.appointment:
            return obj.appointment.appointment_date.strftime("%Y-%m-%d %H:%M")
        return "-"

    get_appointment_date.short_description = "Appointment Date"
    get_appointment_date.admin_order_field = "appointment__appointment_date"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("patient__user", "doctor__user", "appointment")
            .prefetch_related("attachments")
        )

    autocomplete_fields = ["patient", "doctor", "appointment"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "appointment":
            kwargs["queryset"] = (
                MedicalRecord._meta.get_field("appointment")
                .related_model.objects.filter(status="completed")
                .select_related("patient__user", "doctor__user")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ["mark_follow_up_required", "mark_follow_up_not_required"]

    def mark_follow_up_required(self, request, queryset):
        updated = queryset.update(follow_up_required=True)
        self.message_user(
            request, f"{updated} medical records were marked as requiring follow-up."
        )

    mark_follow_up_required.short_description = "Mark as requiring follow-up"

    def mark_follow_up_not_required(self, request, queryset):
        updated = queryset.update(follow_up_required=False)
        self.message_user(
            request,
            f"{updated} medical records were marked as not requiring follow-up.",
        )

    mark_follow_up_not_required.short_description = "Mark as not requiring follow-up"


@admin.register(MedicalRecordAttachment)
class MedicalRecordAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "get_patient_name",
        "get_doctor_name",
        "attachment_type",
        "description",
        "get_file_name",
        "uploaded_at",
    )
    list_filter = (
        "attachment_type",
        "uploaded_at",
        "medical_record__doctor__specialty",
    )
    search_fields = (
        "medical_record__patient__user__first_name",
        "medical_record__patient__user__last_name",
        "medical_record__doctor__user__first_name",
        "medical_record__doctor__user__last_name",
        "description",
        "attachment_type",
    )
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)
    date_hierarchy = "uploaded_at"

    def get_patient_name(self, obj):
        return obj.medical_record.patient.user.full_name

    get_patient_name.short_description = "Patient"
    get_patient_name.admin_order_field = "medical_record__patient__user__first_name"

    def get_doctor_name(self, obj):
        return f"Dr. {obj.medical_record.doctor.user.full_name}"

    get_doctor_name.short_description = "Doctor"
    get_doctor_name.admin_order_field = "medical_record__doctor__user__first_name"

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split("/")[-1]
        return "-"

    get_file_name.short_description = "File Name"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "medical_record__patient__user", "medical_record__doctor__user"
            )
        )

    autocomplete_fields = ["medical_record"]
