from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count
from .models import Booking
from .serializers import (
    BookingSerializer, BookingCreateSerializer,
    BookingListSerializer, BookingApprovalSerializer
)


class BookingPermission(permissions.BasePermission):
    """Custom permission for bookings"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admins can do everything
        if request.user.is_admin():
            return True
        
        # Students and teachers can view and create
        if view.action in ['list', 'retrieve', 'create']:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Admins can do everything
        if request.user.is_admin():
            return True
        
        # Users can only modify their own bookings
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.user == request.user
        
        return True


class BookingViewSet(viewsets.ModelViewSet):
    """API endpoint for managing bookings"""
    queryset = Booking.objects.select_related('user', 'room', 'approved_by')
    permission_classes = [BookingPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'date', 'room', 'user']
    search_fields = ['title', 'description', 'room__name', 'user__email']
    ordering_fields = ['date', 'start_time', 'created_at']
    ordering = ['-date', '-start_time']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action == 'list':
            return BookingListSerializer
        return BookingSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Non-admins can only see their own bookings and approved bookings
        if not user.is_admin():
            queryset = queryset.filter(
                Q(user=user) | Q(status='APPROVED')
            )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter upcoming bookings
        if self.request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(date__gte=timezone.now().date())
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a booking (admin only)"""
        if not request.user.is_admin():
            return Response(
                {'error': 'Only administrators can approve bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking = self.get_object()
        serializer = BookingApprovalSerializer(data={'action': 'approve'})
        serializer.is_valid(raise_exception=True)
        
        booking.approve(request.user)
        
        return Response({
            'message': 'Booking approved successfully',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a booking (admin only)"""
        if not request.user.is_admin():
            return Response(
                {'error': 'Only administrators can reject bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking = self.get_object()
        serializer = BookingApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reason = serializer.validated_data.get('rejection_reason', '')
        booking.reject(request.user, reason)
        
        return Response({
            'message': 'Booking rejected',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Only the booking owner or admin can cancel
        if booking.user != request.user and not request.user.is_admin():
            return Response(
                {'error': 'You can only cancel your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.cancel()
        
        return Response({
            'message': 'Booking cancelled successfully',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get current user's bookings"""
        queryset = self.get_queryset().filter(user=request.user)
        serializer = BookingListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def pending(self, request):
        """Get pending bookings (admin only)"""
        if not request.user.is_admin():
            return Response(
                {'error': 'Only administrators can view pending bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(status='PENDING')
        serializer = BookingListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def check_availability(self, request):
        """Check room availability for a specific date and time"""
        room_id = request.query_params.get('room_id')
        date = request.query_params.get('date')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        
        if not all([room_id, date, start_time, end_time]):
            return Response(
                {'error': 'room_id, date, start_time, and end_time are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            room_id=room_id,
            date=date,
            status__in=['PENDING', 'APPROVED']
        ).exclude(
            Q(end_time__lte=start_time) | Q(start_time__gte=end_time)
        )
        
        is_available = not overlapping.exists()
        
        return Response({
            'available': is_available,
            'conflicting_bookings': BookingListSerializer(overlapping, many=True).data if not is_available else []
        })
