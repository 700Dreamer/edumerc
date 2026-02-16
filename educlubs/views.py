from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication, AskAIQuery
)
from .serializers import (
    MainCategorySerializer,
    SubjectLevelSerializer, SubjectClubSerializer, TopicSerializer, LessonSerializer,
    SocialGroupSerializer, SocialClubSerializer, ClubDiscussionSerializer,
    TeacherCategorySerializer, TeacherClubSerializer,
    RoleModelSerializer, PracticalApplicationSerializer, AskAIQuerySerializer,
    UnifiedClubDetailSerializer
)

class MainCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

class SubCategoryViewSet(viewsets.ViewSet):
    """
    Step 2: Returns sub-categories for a specific main category.
    Dynamic: Returns SubjectLevel, SocialGroup, or TeacherCategory.
    """
    def list(self, request):
        main_cat_id = request.query_params.get('main_category')
        if not main_cat_id:
            return Response({"error": "main_category ID is required"}, status=400)
        
        try:
            main_cat = MainCategory.objects.get(id=main_cat_id)
        except MainCategory.DoesNotExist:
            return Response({"error": "MainCategory not found"}, status=404)

        name = main_cat.name.lower()
        if 'subject' in name:
            data = SubjectLevelSerializer(main_cat.subject_levels.all(), many=True).data
        elif 'social' in name:
            data = SocialGroupSerializer(main_cat.social_groups.all(), many=True).data
        elif 'teacher' in name:
            data = TeacherCategorySerializer(main_cat.teacher_categories.all(), many=True).data
        else:
            data = []
        
        return Response(data)

class ClubViewSet(viewsets.ViewSet):
    """
    Step 3: Returns clubs for a specific sub-category.
    Filter by subcategory_id and type (subject|social|teacher).
    """
    def list(self, request):
        sub_id = request.query_params.get('subcategory_id')
        ctype = request.query_params.get('type') # 'subject', 'social', or 'teacher'

        if not sub_id or not ctype:
            return Response({"error": "subcategory_id and type are required"}, status=400)

        if ctype == 'subject':
            clubs = SubjectClub.objects.filter(level_id=sub_id)
            serializer = SubjectClubSerializer(clubs, many=True)
        elif ctype == 'social':
            clubs = SocialClub.objects.filter(group_id=sub_id)
            serializer = SocialClubSerializer(clubs, many=True)
        elif ctype == 'teacher':
            clubs = TeacherClub.objects.filter(category_id=sub_id)
            serializer = TeacherClubSerializer(clubs, many=True)
        else:
            return Response({"error": "Invalid type"}, status=400)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ctype = request.query_params.get('type')
        if not ctype:
            return Response({"error": "type parameter (subject|social|teacher) is required"}, status=400)

        try:
            if ctype == 'subject':
                obj = SubjectClub.objects.get(pk=pk)
            elif ctype == 'social':
                obj = SocialClub.objects.get(pk=pk)
            elif ctype == 'teacher':
                obj = TeacherClub.objects.get(pk=pk)
            else:
                return Response({"error": "Invalid type"}, status=400)
        except (SubjectClub.DoesNotExist, SocialClub.DoesNotExist, TeacherClub.DoesNotExist):
            return Response({"error": "Club not found"}, status=404)

        serializer = UnifiedClubDetailSerializer(obj)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='curriculum/(?P<club_id>[^/.]+)')
    def curriculum(self, request, club_id=None):
        topics = Topic.objects.filter(club_id=club_id).prefetch_related('lessons')
        return Response(TopicSerializer(topics, many=True).data)

    @action(detail=False, methods=['get'], url_path='discussions/(?P<club_id>[^/.]+)')
    def discussions(self, request, club_id=None):
        discussions = ClubDiscussion.objects.filter(club_id=club_id).order_by('-created_at')
        return Response(ClubDiscussionSerializer(discussions, many=True).data)

# Generic fallback viewsets for administrative CRUD if needed
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ClubDiscussionViewSet(viewsets.ModelViewSet):
    queryset = ClubDiscussion.objects.all()
    serializer_class = ClubDiscussionSerializer
