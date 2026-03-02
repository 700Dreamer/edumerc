from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

import uuid
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment, CoachAvailabilityRange, CoachEarnings, HMSSession, HMSPeer
from payments.models import Withdrawal, Transaction
from payments.pesapal_service import PesaPalService
from django.db.models import Sum
from .serializers import (
    CoachListSerializer, CoachDetailSerializer, 
    SessionSerializer, CoachSessionSerializer, SessionStatusUpdateSerializer,
    VirtualClassSerializer, ClassEnrollmentSerializer, CoachPromotionSerializer,
    WeeklyAvailabilitySerializer, CoachEarningsSerializer, HMSSessionAttendanceSerializer
)

User = get_user_model()

class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoachDetailSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='earnings')
    def earnings(self, request):
        """
        Coach: view financial stats from the ledger.
        """
        if not request.user.is_coach:
            return Response({"detail": "Only coaches can view earnings."}, status=status.HTTP_403_FORBIDDEN)
            
        coach = get_object_or_404(Coach, user=request.user)
        ledger = CoachEarnings.objects.filter(coach=coach)
        
        # Aggregations
        earning = ledger.filter(transaction_type='EARNING', status='EARNED').aggregate(total=Sum('amount'))['total'] or 0.00
        withdrawn = ledger.filter(transaction_type='WITHDRAWAL', status='WITHDRAWN').aggregate(total=Sum('amount'))['total'] or 0.00
        expected = ledger.filter(transaction_type='EARNING', status='EXPECTED').aggregate(total=Sum('amount'))['total'] or 0.00
        
        budget = float(earning) - float(withdrawn)
        
        # Recent transactions
        transactions = ledger.order_by('-created_at')[:20]
        serializer = CoachEarningsSerializer(transactions, many=True)
        
        return Response({
            "Budget": budget,
            "earning": float(earning),
            "withdrawn": float(withdrawn),
            "amount_expected": float(expected),
            "response_obj": serializer.data,
            "currency": "UGX"
        })

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tutor_id = serializer.validated_data.pop('tutor_id', None)
        date_obj = serializer.validated_data.get('date')
        start_time = serializer.validated_data.get('start_time')
        duration = serializer.validated_data.get('duration', 1)
        
        if date_obj < datetime.now().date():
            return Response({"error": "INVALID_DATE", "detail": "Date cannot be in the past."}, status=status.HTTP_400_BAD_REQUEST)

        start_dt = datetime.combine(date_obj, start_time)
        end_dt = start_dt + timedelta(hours=duration)
        end_time = end_dt.time()
        
        try:
            with transaction.atomic():
                # Lock the coach user row to prevent concurrent bookings
                coach_user = User.objects.select_for_update().get(coach_profile__id=tutor_id)
                coach = coach_user.coach_profile
                
                # Double booking check
                overlapping_sessions = CoachingSession.objects.filter(
                    coach=coach,
                    date=date_obj,
                    status__in=['pending', 'confirmed'],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
                
                if overlapping_sessions.exists():
                    return Response({
                        "error": "SLOT_UNAVAILABLE",
                        "detail": f"The selected slot ({start_time.strftime('%H:%M')} on {date_obj}) is no longer available. Please choose a different time."
                    }, status=status.HTTP_409_CONFLICT)
                    
                # Verify slot falls within active ranges
                dow = (date_obj.weekday() + 1) % 7
                active_ranges = CoachAvailabilityRange.objects.filter(coach=coach, day_of_week=dow, is_active=True)
                
                is_within_range = False
                for r in active_ranges:
                    if r.start_time <= start_time and r.end_time >= end_time:
                        is_within_range = True
                        break
                        
                if not is_within_range:
                    return Response({
                        "error": "DURATION_EXCEEDS_RANGE",
                        "detail": "Booking duration overflows coach's available range."
                    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                    
                # TODO: Implement wallet deduction logic here when Wallet model is available
                # current_balance = request.user.wallet.balance
                # required = coach.price_per_hour * duration
                # if current_balance < required:
                #     return Response({"error": "INSUFFICIENT_BALANCE", ...}, status=402)
                
                total_price = coach.price_per_hour * duration
                
                session = serializer.save(
                    student=request.user,
                    coach=coach,
                    total_price=total_price
                )
                
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                
        except User.DoesNotExist:
            return Response({"error": "COACH_NOT_FOUND", "detail": "No active coach with this ID."}, status=status.HTTP_404_NOT_FOUND)

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
        queryset = CoachingSession.objects.filter(coach=coach).order_by('-date', '-start_time')
        serializer = CoachSessionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='initiate-payment')
    def initiate_payment(self, request, pk=None):
        session = self.get_object()
        
        if session.status != 'confirmed':
            return Response(
                {"error": "Session must be confirmed before payment can be initiated."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if session.payment_status == 'paid':
            return Response(
                {"error": "This session has already been paid for."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if session.total_price <= 0:
             return Response(
                {"error": "Invalid session price. Cannot proceed with payment."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if a valid transaction already exists
        if session.transaction and session.transaction.status == 'PENDING' and session.transaction.order_tracking_id:
             return Response(
                 {"error": "A pending payment already exists for this session."},
                 status=status.HTTP_400_BAD_REQUEST
             )
        
        # Create a local Transaction
        merchant_ref = f"EC-PMT-{uuid.uuid4().hex[:8].upper()}"
        transaction_obj = Transaction.objects.create(
            user=request.user,
            amount=session.total_price,
            description=f"Payment for Coaching Session {session.booking_id}",
            merchant_reference=merchant_ref,
            status='PENDING'
        )
        
        session.transaction = transaction_obj
        session.save(update_fields=['transaction'])
        
        pesapal = PesaPalService()
        callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
        order_res = pesapal.submit_order(transaction_obj, callback_url)
        
        if order_res and 'redirect_url' in order_res:
            transaction_obj.order_tracking_id = order_res['order_tracking_id']
            transaction_obj.save(update_fields=['order_tracking_id'])
            
            return Response({
                "redirect_url": order_res['redirect_url'],
                "merchant_reference": merchant_ref,
                "order_tracking_id": order_res['order_tracking_id'],
                "booking_id": session.booking_id
            })
            
        return Response({"error": "Failed to initiate payment with PesaPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='initiate-payment-by-booking/(?P<booking_id>[^/.]+)')
    def initiate_payment_by_booking(self, request, booking_id=None):
        session = get_object_or_404(CoachingSession, booking_id=booking_id)
        
        # Security check: only the student who booked it can initiate payment
        if session.student != request.user:
            return Response({"error": "Unauthorized access to this booking."}, status=status.HTTP_403_FORBIDDEN)

        if session.status != 'confirmed':
            return Response(
                {"error": "Session must be confirmed before payment can be initiated."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if session.payment_status == 'paid':
            return Response(
                {"error": "This session has already been paid for."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if session.total_price <= 0:
             return Response(
                {"error": "Invalid session price. Cannot proceed with payment."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if a valid transaction already exists
        if session.transaction and session.transaction.status == 'PENDING' and session.transaction.order_tracking_id:
             # Instead of erroring, we can return the existing redirect URL if we have it?
             # But PesaPal URLs expire. Better to just allow re-initiation for now or handle it.
             pass
        
        # Create a local Transaction
        merchant_ref = f"EC-PMT-{uuid.uuid4().hex[:8].upper()}"
        transaction_obj = Transaction.objects.create(
            user=request.user,
            amount=session.total_price,
            description=f"Payment for Coaching Session {session.booking_id}",
            merchant_reference=merchant_ref,
            status='PENDING'
        )
        
        session.transaction = transaction_obj
        session.save(update_fields=['transaction'])
        
        pesapal = PesaPalService()
        callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
        order_res = pesapal.submit_order(transaction_obj, callback_url)
        
        if order_res and 'redirect_url' in order_res:
            transaction_obj.order_tracking_id = order_res['order_tracking_id']
            transaction_obj.save(update_fields=['order_tracking_id'])
            
            return Response({
                "redirect_url": order_res['redirect_url'],
                "merchant_reference": merchant_ref,
                "order_tracking_id": order_res['order_tracking_id'],
                "booking_id": session.booking_id
            })
            
        return Response({"error": "Failed to initiate payment with PesaPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='attendance')
    def attendance(self, request, pk=None):
        """Get HMS attendance data for a specific internal session."""
        session = self.get_object()
        hms_session = HMSSession.objects.filter(internal_session=session).order_by('-created_at').first()
        
        if not hms_session:
            return Response({"detail": "No attendance data found for this session."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = HMSSessionAttendanceSerializer(hms_session)
        return Response(serializer.data)

    def update_status_by_booking_id(self, request, booking_id=None):
        """
        Coach: update the status of a specific booking by booking_id.
        Allowed transitions: pending -> confirmed / cancelled
                             confirmed -> completed / cancelled
        """
        if not request.user.is_coach:
            return Response(
                {"detail": "Only coaches can update session status."},
                status=status.HTTP_403_FORBIDDEN
            )
        session = get_object_or_404(CoachingSession, booking_id=booking_id, coach=request.user.coach_profile)
        serializer = SessionStatusUpdateSerializer(
            session, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
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

class CoachAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_coach:
            return Response({"detail": "Only coaches can access availability."}, status=status.HTTP_403_FORBIDDEN)
        
        coach = get_object_or_404(Coach, user=request.user)
        weekly_schedule = []
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        for i, name in enumerate(days):
            ranges_qs = CoachAvailabilityRange.objects.filter(coach=coach, day_of_week=i)
            is_active = ranges_qs.filter(is_active=True).exists()
            if not ranges_qs.exists():
                is_active = False # Default empty day to inactive
                
            day_data = {
                "day_of_week": i,
                "day_name": name,
                "is_active": is_active,
                "ranges": [{"start": r.start_time.strftime("%H:%M"), "end": r.end_time.strftime("%H:%M")} for r in ranges_qs.filter(is_active=True).order_by('start_time')]
            }
            weekly_schedule.append(day_data)
            
        return Response({
            "coach_id": coach.id,
            "weekly_schedule": weekly_schedule
        })

    def put(self, request):
        if not request.user.is_coach:
            return Response({"detail": "Only coaches can access availability."}, status=status.HTTP_403_FORBIDDEN)
            
        coach = get_object_or_404(Coach, user=request.user)
        serializer = WeeklyAvailabilitySerializer(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                CoachAvailabilityRange.objects.filter(coach=coach).delete()
                
                for day_data in serializer.validated_data.get('weekly_schedule', []):
                    day_of_week = day_data['day_of_week']
                    is_active = day_data['is_active']
                    
                    if not is_active:
                        CoachAvailabilityRange.objects.create(
                            coach=coach,
                            day_of_week=day_of_week,
                            start_time="00:00",
                            end_time="00:00",
                            is_active=False
                        )
                    else:
                        for r in day_data.get('ranges', []):
                            CoachAvailabilityRange.objects.create(
                                coach=coach,
                                day_of_week=day_of_week,
                                start_time=r['start_time'],
                                end_time=r['end_time'],
                                is_active=True
                            )
            return Response({"detail": "Availability schedule updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SmartSlotView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        coach = get_object_or_404(Coach, id=id)
        date_str = request.query_params.get('date')
        duration_str = request.query_params.get('duration')
        
        if not date_str or not duration_str:
            return Response({"error": "MISSING_PARAMETERS", "detail": "date and duration are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "INVALID_DATE_FORMAT", "detail": "date must be in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            duration_hours = int(duration_str)
            if duration_hours < 1 or duration_hours > 8:
                raise ValueError()
        except ValueError:
            return Response({"error": "INVALID_DURATION", "detail": "duration must be an integer between 1 and 8."}, status=status.HTTP_400_BAD_REQUEST)
            
        dow = (date_obj.weekday() + 1) % 7 
        ranges = CoachAvailabilityRange.objects.filter(coach=coach, day_of_week=dow, is_active=True)
        
        free_blocks = set()
        for r in ranges:
            cursor = datetime.combine(date_obj, r.start_time)
            end = datetime.combine(date_obj, r.end_time)
            while cursor + timedelta(hours=1) <= end:
                free_blocks.add(cursor.strftime('%H:%M'))
                cursor += timedelta(hours=1)
                
        booked = CoachingSession.objects.filter(coach=coach, date=date_obj, status__in=['pending', 'confirmed'])
        for booking in booked:
            cursor = datetime.combine(date_obj, booking.start_time)
            end = datetime.combine(date_obj, booking.end_time)
            while cursor < end:
                free_blocks.discard(cursor.strftime('%H:%M'))
                cursor += timedelta(hours=1)
                
        valid_slots = []
        for slot in sorted(free_blocks):
            dt = datetime.strptime(slot, '%H:%M')
            if all((dt + timedelta(hours=i)).strftime('%H:%M') in free_blocks for i in range(duration_hours)):
                valid_slots.append(slot)
                
        return Response({
            "coach_id": coach.id,
            "date": date_str,
            "duration_hours": duration_hours,
            "available_slots": valid_slots
        })

class HMSWebhookView(APIView):
    permission_classes = [permissions.AllowAny] # In production, verify signature

    def post(self, request):
        payload = request.data
        event_type = payload.get('type')
        data = payload.get('data')

        if not data:
            return Response({"detail": "No data in payload"}, status=status.HTTP_400_BAD_REQUEST)

        if event_type == 'session.close.success':
            session_id = data.get('id')
            room_id = data.get('room_id')
            
            # Try to find the internal session using the room_id
            # We assume meeting_link contains the room_id (e.g., https://.../meeting/<room_id>)
            internal_session = CoachingSession.objects.filter(
                meeting_link__icontains=room_id
            ).first()

            hms_session, created = HMSSession.objects.update_or_create(
                id=session_id,
                defaults={
                    'room_id': room_id,
                    'internal_session': internal_session,
                    'customer_id': data.get('customer_id'),
                    'app_id': data.get('app_id'),
                    'user_id': data.get('user_id'),
                    'active': data.get('active', False),
                    'created_at': data.get('created_at'),
                    'updated_at': data.get('updated_at'),
                    'ended_at': data.get('ended_at'),
                }
            )

            # Auto-complete the internal coaching session if found
            if internal_session and internal_session.status != 'completed':
                internal_session.status = 'completed'
                internal_session.save(update_fields=['status'])

            peers_data = data.get('peers', {})
            for p_id, p_data in peers_data.items():
                HMSPeer.objects.update_or_create(
                    session=hms_session,
                    peer_id=p_id,
                    defaults={
                        'name': p_data.get('name'),
                        'role': p_data.get('role'),
                        'user_id': p_data.get('user_id'),
                        'joined_at': p_data.get('joined_at'),
                        'left_at': p_data.get('left_at'),
                    }
                )
            
            return Response({"status": "success", "session_id": session_id})

        return Response({"status": "ignored", "event_type": event_type})
