from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment
from .serializers import (
    CoachListSerializer, CoachDetailSerializer, 
    SessionSerializer, CoachSessionSerializer, SessionStatusUpdateSerializer,
    VirtualClassSerializer, ClassEnrollmentSerializer, CoachPromotionSerializer
)

class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoachDetailSerializer
        return super().get_serializer_class()

class PromoteCoachView(generics.CreateAPIView):
    """
    Endpoint to promote the logged-in user to a Coach/Tutor.
    """
    serializer_class = CoachPromotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

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
        """Student: list all sessions booked by the logged-in user."""
        queryset = CoachingSession.objects.filter(student=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-appointments')
    def my_appointments(self, request):
        """
        Coach: list all sessions booked against the logged-in coach.
        Only accessible if the user has a coach profile.
        """
        if not request.user.is_coach:
            return Response(
                {"detail": "Only coaches can view appointments."},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            coach = request.user.coach_profile
        except Coach.DoesNotExist:
            return Response(
                {"detail": "Coach profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = CoachingSession.objects.filter(coach=coach).order_by('-date', '-time')
        serializer = CoachSessionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Coach: update the status of a specific booking.
        Allowed transitions: pending -> confirmed / cancelled
                             confirmed -> completed / cancelled
        """
        if not request.user.is_coach:
            return Response(
                {"detail": "Only coaches can update session status."},
                status=status.HTTP_403_FORBIDDEN
            )
        session = get_object_or_404(CoachingSession, pk=pk, coach=request.user.coach_profile)
        serializer = SessionStatusUpdateSerializer(
            session, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            # Return the full coach view of the updated session
            return Response(
                CoachSessionSerializer(session, context={'request': request}).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
