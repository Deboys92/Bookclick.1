from rest_framework import serializers
from .models import Booking
from rooms.serializers import RoomListSerializer
from accounts.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    user_details = UserSerializer(source='user', read_only=True)
    room_details = RoomListSerializer(source='room', read_only=True)
    is_pending = serializers.ReadOnlyField()
    is_approved = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'user_details', 'room', 'room_details',
            'title', 'description', 'date', 'start_time', 'end_time',
            'status', 'approved_by', 'approval_date', 'rejection_reason',
            'number_of_attendees', 'is_pending', 'is_approved', 'is_past',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'approved_by', 'approval_date',
            'created_at', 'updated_at'
        ]
    
    def validate(self, attrs):
        """Additional validation"""
        # If this is a new booking, set the user from the request
        if not self.instance:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                attrs['user'] = request.user
        
        return attrs


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    
    class Meta:
        model = Booking
        fields = [
            'room', 'title', 'description', 'date',
            'start_time', 'end_time', 'number_of_attendees'
        ]
    
    def create(self, validated_data):
        # Set the user from the request
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for booking list"""
    room_name = serializers.CharField(source='room.name', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'room', 'room_name', 'user_name', 'title',
            'date', 'start_time', 'end_time', 'status'
        ]


class BookingApprovalSerializer(serializers.Serializer):
    """Serializer for booking approval/rejection"""
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        if attrs['action'] == 'reject' and not attrs.get('rejection_reason'):
            raise serializers.ValidationError({
                'rejection_reason': 'Rejection reason is required when rejecting a booking.'
            })
        return attrs
