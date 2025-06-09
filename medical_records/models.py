from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    
    # Medical Information
    chief_complaint = models.TextField()
    history_of_present_illness = models.TextField()
    physical_examination = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True)
    
    # Vital Signs
    blood_pressure = models.CharField(max_length=20, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional Information
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Medical Record - {self.patient.user.full_name} ({self.created_at.date()})"

class MedicalRecordAttachment(models.Model):
    ATTACHMENT_TYPES = (
        ('lab_report', 'Lab Report'),
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct_scan', 'CT Scan'),
        ('prescription', 'Prescription'),
        ('other', 'Other'),
    )
    
    medical_record = models.ForeignKey(
        MedicalRecord, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    file = models.FileField(upload_to='medical_records/')
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPES)
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_attachment_type_display()} - {self.medical_record.patient.user.full_name}"
