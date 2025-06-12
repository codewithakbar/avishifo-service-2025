# appointments/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    # Basic Information
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='patient_appointments',
        limit_choices_to={'user_type': 'patient'}
    )
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='doctor_appointments',
        limit_choices_to={'user_type': 'doctor'}
    )
    
    # Appointment Details
    requested_date = models.DateField()
    requested_time = models.TimeField()
    reason = models.CharField(max_length=200)
    description = models.TextField()
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Patient Contact Info (can be different from profile)
    patient_phone = models.CharField(max_length=17, blank=True)
    patient_email = models.EmailField(blank=True)
    
    # Additional Info
    patient_history_notes = models.TextField(blank=True)
    
    # Status Change Tracking
    confirmed_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['doctor', 'status']),
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['requested_date', 'requested_time']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name} ({self.requested_date})"
    
    @property
    def patient_age(self):
        if self.patient.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.patient.date_of_birth.year - (
                (today.month, today.day) < (self.patient.date_of_birth.month, self.patient.date_of_birth.day)
            )
        return None