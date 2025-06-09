import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_api.settings')
django.setup()

from accounts.models import User
from hospitals.models import Hospital
from doctors.models import Doctor, DoctorSchedule
from patients.models import Patient
from appointments.models import Appointment

def seed_data():
    """Seed the database with sample data"""
    
    print("Creating sample data...")
    
    # Create Hospital
    hospital, created = Hospital.objects.get_or_create(
        name="City General Hospital",
        defaults={
            'address': '123 Main Street, Tashkent, Uzbekistan',
            'phone_number': '+998901234567',
            'email': 'info@citygeneral.uz',
            'website': 'https://citygeneral.uz',
            'license_number': 'LIC001',
            'established_date': datetime(2000, 1, 1).date(),
            'bed_capacity': 200,
            'emergency_services': True,
        }
    )
    
    # Create Doctor User
    doctor_user, created = User.objects.get_or_create(
        username='dr_sarah',
        defaults={
            'email': 'sarah.johnson@hospital.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'user_type': 'doctor',
            'phone_number': '+998901234568',
            'is_verified': True,
        }
    )
    if created:
        doctor_user.set_password('doctor123')
        doctor_user.save()
    
    # Create Doctor Profile
    doctor, created = Doctor.objects.get_or_create(
        user=doctor_user,
        defaults={
            'specialty': 'cardiology',
            'license_number': 'DOC001',
            'hospital': hospital,
            'years_of_experience': 10,
            'education': 'MD from Tashkent Medical Academy',
            'certifications': 'Board Certified Cardiologist',
            'consultation_fee': Decimal('150000.00'),
            'rating': Decimal('4.8'),
        }
    )
    
    # Create Doctor Schedule
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    for day in days:
        DoctorSchedule.objects.get_or_create(
            doctor=doctor,
            day_of_week=day,
            defaults={
                'start_time': '09:00',
                'end_time': '17:00',
                'is_available': True,
            }
        )
    
    # Create Patient User
    patient_user, created = User.objects.get_or_create(
        username='john_doe',
        defaults={
            'email': 'john.doe@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'patient',
            'phone_number': '+998901234569',
            'date_of_birth': datetime(1985, 1, 15).date(),
            'address': '456 Oak Street, Tashkent, Uzbekistan',
            'is_verified': True,
        }
    )
    if created:
        patient_user.set_password('patient123')
        patient_user.save()
    
    # Create Patient Profile
    patient, created = Patient.objects.get_or_create(
        user=patient_user,
        defaults={
            'blood_type': 'O+',
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_phone': '+998901234570',
            'medical_history': 'No significant medical history',
            'allergies': 'None known',
            'current_medications': 'None',
            'insurance_number': 'INS001',
        }
    )
    
    # Create Sample Appointment
    appointment_date = datetime.now() + timedelta(days=7)
    appointment, created = Appointment.objects.get_or_create(
        patient=patient,
        doctor=doctor,
        appointment_date=appointment_date,
        defaults={
            'appointment_type': 'consultation',
            'reason': 'Regular check-up',
            'status': 'scheduled',
            'duration_minutes': 30,
        }
    )
    
    print("Sample data created successfully!")
    print("\nLogin credentials:")
    print("Doctor - Username: dr_sarah, Password: doctor123")
    print("Patient - Username: john_doe, Password: patient123")
    print("Admin - Username: admin, Password: admin123")

if __name__ == '__main__':
    seed_data()
