from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    equipment_list = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'name', 'room_type', 'building', 'floor', 'capacity',
            'description', 'status', 'has_projector', 'has_whiteboard',
            'has_computer', 'has_wifi', 'has_ac', 'has_audio_system',
            'image', 'equipment_list', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoomListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for room list"""
    equipment_list = serializers.ReadOnlyField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'name', 'room_type', 'building', 'capacity',
            'status', 'equipment_list'
        ]
