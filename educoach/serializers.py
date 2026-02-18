from rest_framework import serializers
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment
from django.db import transaction

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

class CoachPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = [
            'title', 'experience', 'price_per_hour', 
            'description', 'subjects', 'levels', 'badges'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        
        with transaction.atomic():
            # Update user role to TEACHER and flag as coach
            if user.role != 'TEACHER':
                user.role = 'TEACHER'
            user.is_coach = True
            user.save()
            
            # Create or update Coach profile
            coach, created = Coach.objects.update_or_create(
                user=user,
                defaults=validated_data
            )
            
        return coach

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


class CoachSessionSerializer(serializers.ModelSerializer):
    """Session view from the coach's perspective — shows student details."""
    booking_id = serializers.SerializerMethodField(read_only=True)
    student_name = serializers.SerializerMethodField(read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)

    class Meta:
        model = CoachingSession
        fields = [
            'booking_id', 'status', 'student_name', 'student_email',
            'date', 'time', 'duration', 'total_price',
            'meeting_link', 'note', 'created_at',
        ]
        read_only_fields = fields

    def get_booking_id(self, obj):
        return f"BK-{obj.id}"

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username


class SessionStatusUpdateSerializer(serializers.ModelSerializer):
    """Allows a coach to transition a session status."""
    ALLOWED_STATUSES = ['confirmed', 'cancelled', 'completed']

    status = serializers.ChoiceField(choices=ALLOWED_STATUSES)
    meeting_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = CoachingSession
        fields = ['status', 'meeting_link']

    def validate_status(self, value):
        instance = self.instance
        # Cannot change a session that is already cancelled or completed
        if instance and instance.status in ('cancelled', 'completed'):
            raise serializers.ValidationError(
                f"Cannot update a session that is already '{instance.status}'."
            )
        return value

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
