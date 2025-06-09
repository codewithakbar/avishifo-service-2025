from django.db import models
from accounts.models import User
from hospitals.models import Hospital

class Doctor(models.Model):
    SPECIALTIES = (
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('general', 'General Medicine'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_id = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.get_specialty_display()}"
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            # Generate doctor ID
            last_doctor = Doctor.objects.order_by('-id').first()
            if last_doctor:
                last_id = int(last_doctor.doctor_id[1:])
                self.doctor_id = f"D{last_id + 1:06d}"
            else:
                self.doctor_id = "D000001"
        super().save(*args, **kwargs)

class DoctorSchedule(models.Model):
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.get_day_of_week_display()}"
