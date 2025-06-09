import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_api.settings')
django.setup()

from accounts.models import User

def create_superuser():
    """Create a superuser for the application"""
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
        return
    
    # Create superuser
    superuser = User.objects.create_user(
        username='admin',
        email='admin@healthcare.com',
        password='admin123',
        first_name='Super',
        last_name='Admin',
        user_type='super_admin',
        is_staff=True,
        is_superuser=True,
        is_verified=True
    )
    
    print(f"Superuser created successfully!")
    print(f"Username: {superuser.username}")
    print(f"Email: {superuser.email}")
    print(f"Password: admin123")

if __name__ == '__main__':
    create_superuser()
