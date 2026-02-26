from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from rooms.models import Room


class Booking(models.Model):
    """
    Model representing a room booking/reservation
    """
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text='User who made the booking'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text='Room being booked'
    )
    
    # Booking details
    title = models.CharField(
        max_length=200,
        help_text='Purpose/title of the booking (e.g., Math Class, Team Meeting)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Additional details about the booking'
    )
    
    # Date and time
    date = models.DateField(help_text='Start date of the booking')
    end_date = models.DateField(
        null=True, 
        blank=True,
        help_text='End date for multi-day bookings (leave empty for a single day)'
    )
    start_time = models.TimeField(help_text='Start time of the booking')
    end_time = models.TimeField(help_text='End time of the booking')
    
    # Status and approval
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_bookings',
        help_text='Admin who approved/rejected the booking'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Attendance
    number_of_attendees = models.PositiveIntegerField(
        default=1,
        help_text='Expected number of attendees'
    )
    
    # Notifications
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        indexes = [
            models.Index(fields=['date', 'start_time']),
            models.Index(fields=['status']),
            models.Index(fields=['room', 'date']),
        ]
    
    def __str__(self):
        return f"{self.room.name} - {self.date} ({self.start_time}-{self.end_time})"
    
    def clean(self):
        """Validate booking data"""
        # Check if end time is after start time
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError('End time must be after start time')
        
        # Check if booking date is not in the past
        if self.date and self.date < timezone.now().date():
            raise ValidationError('Cannot book a room for a past date')
        
        # Check if number of attendees doesn't exceed room capacity
        if self.number_of_attendees and self.room:
            if self.number_of_attendees > self.room.capacity:
                raise ValidationError(
                    f'Number of attendees ({self.number_of_attendees}) exceeds room capacity ({self.room.capacity})'
                )
        
        # Check for overlapping bookings
        if self.room and self.date and self.start_time and self.end_time:
            overlapping = Booking.objects.filter(
                room=self.room,
                date=self.date,
                status__in=['PENDING', 'APPROVED']
            ).exclude(pk=self.pk)
            
            for booking in overlapping:
                # Check if times overlap
                if (self.start_time < booking.end_time and self.end_time > booking.start_time):
                    raise ValidationError(
                        f'This room is already booked from {booking.start_time} to {booking.end_time}'
                    )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_pending(self):
        return self.status == 'PENDING'
    
    @property
    def is_approved(self):
        return self.status == 'APPROVED'
    
    @property
    def is_past(self):
        """Check if booking is in the past"""
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.end_time)
        )
        return booking_datetime < timezone.now()
    
    def approve(self, admin_user):
        """Approve the booking"""
        self.status = 'APPROVED'
        self.approved_by = admin_user
        self.approval_date = timezone.now()
        self.save()
        
        # Send approval email
        try:
            from .emails import send_booking_approval_email
            send_booking_approval_email(self)
        except Exception as e:
            print(f"Error sending approval email: {e}")
    
    def reject(self, admin_user, reason=''):
        """Reject the booking"""
        self.status = 'REJECTED'
        self.approved_by = admin_user
        self.approval_date = timezone.now()
        self.rejection_reason = reason
        self.save()
        
        # Send rejection email
        try:
            from .emails import send_booking_rejection_email
            send_booking_rejection_email(self)
        except Exception as e:
            print(f"Error sending rejection email: {e}")
    
    def cancel(self):
        """Cancel the booking"""
        self.status = 'CANCELLED'
        self.save()
        
        # Send cancellation email
        try:
            from .emails import send_booking_cancellation_email
            send_booking_cancellation_email(self)
        except Exception as e:
            print(f"Error sending cancellation email: {e}")
