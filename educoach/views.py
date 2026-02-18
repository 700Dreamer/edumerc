from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment
from .serializers import (
    CoachListSerializer, CoachDetailSerializer, 
    SessionSerializer, VirtualClassSerializer, 
    ClassEnrollmentSerializer
)

class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoachDetailSerializer
        return super().get_serializer_class()

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'coach_profile'):
            return CoachingSession.objects.filter(coach=user.coach_profile)
        return CoachingSession.objects.filter(student=user)

    def perform_create(self, serializer):
        coach_id = serializer.validated_data.pop('tutor_id')
        coach = get_object_or_404(Coach, id=coach_id)
        
        # Calculate price
        duration = serializer.validated_data.get('duration', 1)
        total_price = coach.price_per_hour * duration
        
        serializer.save(
            student=self.request.user,
            coach=coach,
            total_price=total_price
        )

    @action(detail=False, methods=['get'], url_path='my-bookings')
    def my_bookings(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class VirtualClassViewSet(viewsets.ModelViewSet):
    queryset = VirtualClass.objects.all()
    serializer_class = VirtualClassSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            # Ideally only teachers/admins
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        virtual_class = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
            
        if virtual_class.enrollments.filter(student=user).exists():
            return Response({"detail": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)
            
        if virtual_class.enrolled_count >= virtual_class.capacity:
            return Response({"detail": "Class is full."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClassEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=user, virtual_class=virtual_class)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
