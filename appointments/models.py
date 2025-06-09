from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    APPOINTMENT_TYPES = (
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('check_up', 'Check-up'),
        ('emergency', 'Emergency'),
        ('surgery', 'Surgery'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"{self.patient.user.full_name} - {self.doctor.user.full_name} ({self.appointment_date})"
    
    def save(self, *args, **kwargs):
        if not self.fee:
            self.fee = self.doctor.consultation_fee
        super().save(*args, **kwargs)
