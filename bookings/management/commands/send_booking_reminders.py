from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking
from bookings.emails import send_booking_reminder_email


class Command(BaseCommand):
    help = 'Send reminder emails for bookings happening in the next 24 hours'

    def handle(self, *args, **options):
        # Get tomorrow's date
        tomorrow = timezone.now().date() + timedelta(days=1)
        
        # Get approved bookings for tomorrow that haven't been reminded
        bookings = Booking.objects.filter(
            date=tomorrow,
            status='APPROVED',
            reminder_sent=False
        )
        
        sent_count = 0
        for booking in bookings:
            try:
                if send_booking_reminder_email(booking):
                    booking.reminder_sent = True
                    booking.save()
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Reminder sent for booking #{booking.id}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error sending reminder for booking #{booking.id}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {sent_count} reminder(s)')
        )
