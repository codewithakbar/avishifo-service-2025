from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hospital
from .serializers import HospitalSerializer, HospitalCreateSerializer

class HospitalListView(generics.ListCreateAPIView):
    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'established_date', 'bed_capacity']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HospitalCreateSerializer
        return HospitalSerializer

class HospitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAuthenticated]
