from rest_framework import viewsets, permissions
from .models import Material, MaterialOrder
from .serializers import MaterialSerializer, MaterialOrderSerializer

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filterset_fields = ['material_type', 'session']

class MaterialOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialOrderSerializer

    def get_queryset(self):
        return MaterialOrder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
