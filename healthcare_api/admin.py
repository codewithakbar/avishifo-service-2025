from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html


class HealthcareAdminSite(AdminSite):
    site_header = "Healthcare Management System"
    site_title = "Healthcare Admin"
    index_title = "Welcome to Healthcare Administration"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Add custom statistics to admin index
        from accounts.models import User
        from patients.models import Patient
        from doctors.models import Doctor
        from appointments.models import Appointment
        from medical_records.models import MedicalRecord
        from hospitals.models import Hospital

        stats = {
            "total_users": User.objects.count(),
            "total_patients": Patient.objects.count(),
            "total_doctors": Doctor.objects.count(),
            "total_hospitals": Hospital.objects.count(),
            "total_appointments": Appointment.objects.count(),
            "total_medical_records": MedicalRecord.objects.count(),
            "pending_appointments": Appointment.objects.filter(
                status="scheduled"
            ).count(),
            "active_doctors": Doctor.objects.filter(is_available=True).count(),
        }

        extra_context["stats"] = stats
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = HealthcareAdminSite(name="healthcare_admin")

# Customize admin interface
admin.site.site_header = "Healthcare Management System"
admin.site.site_title = "Healthcare Admin"
admin.site.index_title = "Welcome to Healthcare Administration"

# Add custom CSS
admin.site.enable_nav_sidebar = True
