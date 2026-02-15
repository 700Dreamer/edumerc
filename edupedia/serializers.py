from rest_framework import serializers
from .models import School, SchoolGalleryImage, SchoolEvent, SchoolAdministrator, PromotionalMaterial, SchoolReview

class SchoolGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGalleryImage
        fields = '__all__'

class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = '__all__'

class SchoolAdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAdministrator
        fields = '__all__'

class PromotionalMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalMaterial
        fields = '__all__'

class SchoolReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = SchoolReview
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class SchoolSerializer(serializers.ModelSerializer):
    gallery = SchoolGalleryImageSerializer(many=True, read_only=True)
    events = SchoolEventSerializer(many=True, read_only=True)
    administrators = SchoolAdministratorSerializer(many=True, read_only=True)
    promotional_materials = PromotionalMaterialSerializer(many=True, read_only=True)
    reviews = SchoolReviewSerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = '__all__'
        lookup_field = 'slug'
