# appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient', 'doctor', 'requested_date', 'requested_time', 
        'status', 'priority', 'created_at'
    ]
    list_filter = ['status', 'priority', 'requested_date', 'created_at']
    search_fields = [
        'patient__first_name', 'patient__last_name', 
        'doctor__first_name', 'doctor__last_name',
        'reason', 'description'
    ]
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'rejected_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'doctor', 'requested_date', 'requested_time')
        }),
        ('Appointment Details', {
            'fields': ('reason', 'description', 'status', 'priority')
        }),
        ('Contact Information', {
            'fields': ('patient_phone', 'patient_email')
        }),
        ('Additional Notes', {
            'fields': ('patient_history_notes', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'rejected_at'),
            'classes': ('collapse',)
        }),
    )