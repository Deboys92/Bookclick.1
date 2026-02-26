from django.db import models
from django.core.validators import MinValueValidator


class Room(models.Model):
    """
    Model representing a bookable room/space on campus
    """
    
    ROOM_TYPE_CHOICES = (
        ('CLASSROOM', 'Classroom'),
        ('LABORATORY', 'Laboratory'),
        ('AUDITORIUM', 'Auditorium'),
        ('MEETING_ROOM', 'Meeting Room'),
        ('CONFERENCE_HALL', 'Conference Hall'),
        ('STUDY_ROOM', 'Study Room'),
        ('OTHER', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('UNAVAILABLE', 'Unavailable'),
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Room name or number (e.g., Room 101, Lab A)'
    )
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES,
        default='CLASSROOM'
    )
    building = models.CharField(
        max_length=100,
        help_text='Building name or location'
    )
    floor = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Floor number'
    )
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Maximum number of people'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Additional information about the room'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )
    
    # Equipment/Amenities
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    has_computer = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False, verbose_name='Has Air Conditioning')
    has_audio_system = models.BooleanField(default=False)
    
    # Images
    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True,
        help_text='Room photo'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['building', 'name']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.name} - {self.building}"
    
    @property
    def is_available(self):
        return self.status == 'AVAILABLE'
    
    @property
    def equipment_list(self):
        """Returns a list of available equipment"""
        equipment = []
        if self.has_projector:
            equipment.append('Projector')
        if self.has_whiteboard:
            equipment.append('Whiteboard')
        if self.has_computer:
            equipment.append('Computer')
        if self.has_wifi:
            equipment.append('Wi-Fi')
        if self.has_ac:
            equipment.append('Air Conditioning')
        if self.has_audio_system:
            equipment.append('Audio System')
        return equipment
