from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment
from .serializers import (
    SectionSerializer, LevelSerializer, SubjectSerializer, 
    TopicSerializer, SubtopicSerializer, LessonSerializer, AssessmentSerializer,
    SubjectDetailSerializer, TopicDetailSerializer, SubtopicDetailSerializer, 
    LessonDetailSerializer
)

class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]

class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['section']
    ordering_fields = ['order', 'name']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['level', 'level__section']
    ordering_fields = ['order', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubjectDetailSerializer
        return super().get_serializer_class()

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subject']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TopicDetailSerializer
        return super().get_serializer_class()

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['topic']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubtopicDetailSerializer
        return super().get_serializer_class()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subtopic', 'is_published']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return super().get_serializer_class()

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lesson']
    ordering_fields = ['order', 'title']

# ---------------------------------------------------------------------------
# Club endpoints (public, no auth required)
# ---------------------------------------------------------------------------

from .club_models import Club
from .serializers import ClubSerializer, ClubDetailSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

class ClubPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ClubListAPIView(viewsets.ReadOnlyModelViewSet):
    """Paginated list of clubs and retrieve detail. Public – allow any."""
    permission_classes = [permissions.AllowAny]
    pagination_class = ClubPagination

    def get_queryset(self):
        if self.action == 'retrieve':
            return Club.objects.prefetch_related(
                'notes',
                'role_models',
                'practical',
                'discussion',
                'level__subjects__topics__subtopics__lessons__assessments'
            ).select_related('level').all()
            
        queryset = Club.objects.select_related('level').all()
        subcategory_id = self.request.query_params.get('subcategory_id')
        club_type = self.request.query_params.get('type')
        if subcategory_id:
            queryset = queryset.filter(level_id=subcategory_id)
        if club_type:
            queryset = queryset.filter(type=club_type)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClubDetailSerializer
        return ClubSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Optional filtering based on ?type=
        club_type = request.query_params.get('type')
        if club_type and club_type != instance.type:
            # Return empty sections for mismatched type
            for key in ['curriculum', 'notes', 'roleModels', 'practical', 'discussion']:
                data[key] = [] if isinstance(data.get(key), list) else None
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='join')
    def join(self, request, pk=None):
        club = self.get_object()
        user = request.user
        
        # 1. Check if user already has an active subscription
        from django.utils import timezone
        from django.db.models import Q
        active_sub = club.subscriptions.filter(user=user, status='active').filter(
            Q(expires_at__gt=timezone.now()) | Q(expires_at__isnull=True)
        ).first()
        
        if active_sub:
            return Response({"error": "You are already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)
            
        # 2. Check if there's a pending subscription with an active/pending transaction to avoid duplicates
        pending_sub = club.subscriptions.filter(user=user, status='pending').first()
        if pending_sub and pending_sub.transaction and pending_sub.transaction.status == 'PENDING' and pending_sub.transaction.order_tracking_id:
            transaction_obj = pending_sub.transaction
        else:
            # Create new Transaction
            import uuid
            from payments.models import Transaction
            merchant_ref = f"EC-CLUB-{uuid.uuid4().hex[:8].upper()}"
            transaction_obj = Transaction.objects.create(
                user=user,
                amount=club.price,
                description=f"Subscription for Club: {club.name}",
                merchant_reference=merchant_ref,
                transaction_type='CLUB',
                status='PENDING'
            )
            
            # Create or update subscription linking it to this transaction
            if pending_sub:
                pending_sub.transaction = transaction_obj
                pending_sub.save(update_fields=['transaction'])
            else:
                from .club_models import ClubSubscription
                ClubSubscription.objects.create(
                    user=user,
                    club=club,
                    transaction=transaction_obj,
                    status='pending'
                )
        
        # 3. Call PesaPal to get payment URL
        from payments.pesapal_service import PesaPalService
        from django.conf import settings
        pesapal = PesaPalService()
        callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
        order_res = pesapal.submit_order(transaction_obj, callback_url)
        
        if order_res and 'redirect_url' in order_res:
            transaction_obj.order_tracking_id = order_res['order_tracking_id']
            transaction_obj.save(update_fields=['order_tracking_id'])
            return Response({
                "redirect_url": order_res['redirect_url'],
                "merchant_reference": transaction_obj.merchant_reference,
                "order_tracking_id": order_res['order_tracking_id']
            })
            
        return Response({"error": "Failed to initiate payment with PesaPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from .club_models import DiscussionMessage
from .serializers import DiscussionMessageSerializer

class MainCategoriesView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        data = [
            { "id": 1, "name": "Subject Clubs", "description": "Academic mastery." },
            { "id": 2, "name": "Social Clubs", "description": "Hobbies and arts.", "comingSoon": True },
            { "id": 3, "name": "Teacher Clubs", "description": "Collaboration." }
        ]
        return Response(data, status=status.HTTP_200_OK)

class SubCategoriesView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        from .models import Level
        levels = Level.objects.all().order_by('order')
        data = [{'id': level.id, 'name': level.name} for level in levels]
        return Response(data, status=status.HTTP_200_OK)

class AIAssistView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        query = request.data.get('query', '').lower()
        if 'photosynthesis' in query:
            response_text = "Photosynthesis is the process used by plants to convert light energy into chemical energy. In desert plants, this often happens via CAM photosynthesis to conserve water."
        elif 'artery' in query or 'vein' in query:
            response_text = "Arteries carry oxygenated blood away from the heart to the body, whereas veins carry deoxygenated blood back to the heart."
        elif 'equation' in query:
            response_text = "An equation is a mathematical statement asserting the equality of two expressions. To solve, perform the same operation on both sides."
        else:
            response_text = "That is a great question! Based on the curriculum context for this club, you should focus on the core concepts, definitions, and practical examples outlined in the modules."
        return Response({"response": response_text}, status=status.HTTP_200_OK)

class DiscussionMessageViewSet(viewsets.ModelViewSet):
    queryset = DiscussionMessage.objects.select_related('user').all()
    serializer_class = DiscussionMessageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        user = self.request.user
        if not user or user.is_anonymous:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        club = serializer.validated_data.get('club')
        if club:
            from django.utils import timezone
            from django.db.models import Q
            is_sub = user.is_superuser or club.subscriptions.filter(
                user=user,
                status='active'
            ).filter(
                Q(expires_at__gt=timezone.now()) | Q(expires_at__isnull=True)
            ).exists()
            
            if not is_sub:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You must pay and join this club to participate in the discussions.")

        serializer.save(user=user)

