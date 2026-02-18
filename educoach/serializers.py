from rest_framework import serializers
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment

class CoachListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='price_per_hour', max_digits=10, decimal_places=2)
    online = serializers.BooleanField(source='is_active')

    class Meta:
        model = Coach
        fields = [
            'id', 'name', 'title', 'avatar', 'subjects', 'levels', 
            'rating', 'review_count', 'experience', 'price', 
            'description', 'online', 'badges'
        ]

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_avatar(self, obj):
        if hasattr(obj.user, 'profile') and obj.user.profile.avatar:
            return obj.user.profile.avatar.url
        return None

class CoachDetailSerializer(CoachListSerializer):
    pass

class SessionSerializer(serializers.ModelSerializer):
    tutor_id = serializers.IntegerField(write_only=True)
    tutor_name = serializers.CharField(source='coach.user.get_full_name', read_only=True)
    booking_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CoachingSession
        fields = [
            'booking_id', 'status', 'tutor_name', 'tutor_id',
            'date', 'time', 'total_price', 'meeting_link',
            'note', 'duration'
        ]
        read_only_fields = ['status', 'total_price', 'meeting_link', 'booking_id']

    def get_booking_id(self, obj):
        return f"BK-{obj.id}"

class VirtualClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='coach.user.get_full_name', read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = VirtualClass
        fields = [
            'id', 'title', 'teacher_name', 'subject', 'level',
            'start_date', 'schedule', 'duration_weeks', 'price',
            'capacity', 'enrolled_count', 'description', 'is_enrolled'
        ]

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(student=request.user).exists()
        return False

class ClassEnrollmentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ClassEnrollment
        fields = ['student_id', 'payment_reference']
