from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=17)
    email = models.EmailField()
    website = models.URLField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    established_date = models.DateField()
    bed_capacity = models.PositiveIntegerField(default=0)
    emergency_services = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_doctors(self):
        return self.doctors.count()
    
    @property
    def available_doctors(self):
        return self.doctors.filter(is_available=True).count()

class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    head_doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.name}"

    class Meta:
        db_table = 'departments'
        unique_together = ['hospital', 'name']
