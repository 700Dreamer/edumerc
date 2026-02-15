from rest_framework import serializers
from .models import Material, MaterialOrder

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialOrderSerializer(serializers.ModelSerializer):
    material_title = serializers.CharField(source='material.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MaterialOrder
        fields = ['id', 'user', 'username', 'material', 'material_title', 'status', 'ordered_at']
        read_only_fields = ['user', 'status']
