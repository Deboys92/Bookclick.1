from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'room_type', 'capacity', 'status', 'created_at']
    list_filter = ['room_type', 'status', 'building', 'has_projector', 'has_wifi']
    search_fields = ['name', 'building', 'description']
    ordering = ['building', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'room_type', 'building', 'floor', 'capacity', 'description', 'status')
        }),
        ('Equipment & Amenities', {
            'fields': ('has_projector', 'has_whiteboard', 'has_computer', 'has_wifi', 'has_ac', 'has_audio_system')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
