from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_booking_confirmation_email(booking):
    """Send email when booking is created"""
    subject = f'Booking Confirmation - {booking.room.name}'
    
    message = f"""
    Dear {booking.user.get_full_name()},
    
    Your booking request has been received and is pending approval.
    
    Booking Details:
    - Room: {booking.room.name}
    - Building: {booking.room.building}
    - Date: {booking.date.strftime('%B %d, %Y')}
    - Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    - Attendees: {booking.number_of_attendees}
    
    You will receive another email once your booking is approved or rejected.
    
    Best regards,
    BookClick Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_approval_email(booking):
    """Send email when booking is approved"""
    subject = f'Booking Approved - {booking.room.name}'
    
    message = f"""
    Dear {booking.user.get_full_name()},
    
    Great news! Your booking has been APPROVED.
    
    Booking Details:
    - Room: {booking.room.name}
    - Building: {booking.room.building}
    - Date: {booking.date.strftime('%B %d, %Y')}
    - Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    - Attendees: {booking.number_of_attendees}
    
    Please arrive on time and ensure the room is left in good condition.
    
    Best regards,
    BookClick Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_rejection_email(booking):
    """Send email when booking is rejected"""
    subject = f'Booking Rejected - {booking.room.name}'
    
    message = f"""
    Dear {booking.user.get_full_name()},
    
    We regret to inform you that your booking has been REJECTED.
    
    Booking Details:
    - Room: {booking.room.name}
    - Date: {booking.date.strftime('%B %d, %Y')}
    - Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    
    Reason: {booking.rejection_reason or 'Not specified'}
    
    Please feel free to submit a new booking request for a different time or room.
    
    Best regards,
    BookClick Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_cancellation_email(booking):
    """Send email when booking is cancelled"""
    subject = f'Booking Cancelled - {booking.room.name}'
    
    message = f"""
    Dear {booking.user.get_full_name()},
    
    Your booking has been CANCELLED.
    
    Booking Details:
    - Room: {booking.room.name}
    - Date: {booking.date.strftime('%B %d, %Y')}
    - Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    
    If you did not request this cancellation, please contact the administrator.
    
    Best regards,
    BookClick Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_reminder_email(booking):
    """Send reminder email 24 hours before booking"""
    subject = f'Booking Reminder - {booking.room.name}'
    
    message = f"""
    Dear {booking.user.get_full_name()},
    
    This is a reminder for your upcoming booking tomorrow.
    
    Booking Details:
    - Room: {booking.room.name}
    - Building: {booking.room.building}
    - Date: {booking.date.strftime('%B %d, %Y')}
    - Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    - Attendees: {booking.number_of_attendees}
    
    Please arrive on time. If you need to cancel, please do so as soon as possible.
    
    Best regards,
    BookClick Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_admin_notification_email(booking):
    """Send notification to admins when new booking is created"""
    from accounts.models import User
    
    subject = f'New Booking Request - {booking.room.name}'
    
    message = f"""
    A new booking request has been submitted and requires approval.
    
    User: {booking.user.get_full_name()} ({booking.user.email})
    Room: {booking.room.name}
    Building: {booking.room.building}
    Date: {booking.date.strftime('%B %d, %Y')}
    Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    Attendees: {booking.number_of_attendees}
    
    Please review and approve/reject this booking.
    
    BookClick System
    """
    
    # Get all admin users
    admin_emails = User.objects.filter(role='ADMIN', is_active=True).values_list('email', flat=True)
    
    if admin_emails:
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                list(admin_emails),
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    return False
