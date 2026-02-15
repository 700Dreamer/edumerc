from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import School, SchoolEvent, SchoolReview
from .serializers import SchoolSerializer, SchoolEventSerializer, SchoolReviewSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = 'slug'
    filterset_fields = ['location']

    @action(detail=True, methods=['get'])
    def events(self, request, slug=None):
        school = self.get_object()
        events = school.events.all()
        serializer = SchoolEventSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def reviews(self, request, slug=None):
        school = self.get_object()
        if request.method == 'POST':
            serializer = SchoolReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(school=school, user=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        
        reviews = school.reviews.all()
        serializer = SchoolReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class SchoolEventViewSet(viewsets.ModelViewSet):
    queryset = SchoolEvent.objects.all()
    serializer_class = SchoolEventSerializer
