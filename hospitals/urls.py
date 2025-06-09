from django.urls import path
from .views import HospitalListView, HospitalDetailView

urlpatterns = [
    path('', HospitalListView.as_view(), name='hospital-list'),
    path('<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
]
