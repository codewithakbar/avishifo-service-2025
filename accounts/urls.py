from django.urls import path
from .views import (
    UserRegistrationView, UserProfileView,
    ChangePasswordView, user_dashboard_stats
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('dashboard-stats/', user_dashboard_stats, name='dashboard-stats'),
]
