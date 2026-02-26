from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room
from .serializers import RoomSerializer, RoomListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission: only admins can create/update/delete"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin()


class RoomViewSet(viewsets.ModelViewSet):
    """API endpoint for managing rooms"""
    queryset = Room.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room_type', 'building', 'status', 'capacity']
    search_fields = ['name', 'building', 'description']
    ordering_fields = ['name', 'capacity', 'created_at']
    ordering = ['building', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        return RoomSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by equipment
        if self.request.query_params.get('has_projector') == 'true':
            queryset = queryset.filter(has_projector=True)
        if self.request.query_params.get('has_wifi') == 'true':
            queryset = queryset.filter(has_wifi=True)
        if self.request.query_params.get('has_computer') == 'true':
            queryset = queryset.filter(has_computer=True)
        
        # Filter by minimum capacity
        min_capacity = self.request.query_params.get('min_capacity')
        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)
        
        return queryset
