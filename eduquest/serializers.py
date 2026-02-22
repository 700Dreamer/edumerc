from rest_framework import serializers
from .models import Material, MaterialOrder

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialOrderSerializer(serializers.ModelSerializer):
    material_title = serializers.CharField(source='material.title', read_only=True)
    username       = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MaterialOrder
        fields = [
            'id', 'reference', 'username', 'user',
            'material', 'material_title',
            'session',
            'school_name', 'representative', 'location',
            'address', 'phone', 'email', 'delivery_date',
            'levels_data', 'total_sets', 'estimated_amount',
            'status', 'transaction', 'ordered_at'
        ]
        read_only_fields = ['user', 'status', 'reference', 'transaction', 'ordered_at']
