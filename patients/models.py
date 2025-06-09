from django.db import models
from accounts.models import User

class Patient(models.Model):
    BLOOD_TYPES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Patient: {self.user.full_name} ({self.patient_id})"
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate patient ID
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                last_id = int(last_patient.patient_id[1:])
                self.patient_id = f"P{last_id + 1:06d}"
            else:
                self.patient_id = "P000001"
        super().save(*args, **kwargs)
