# Email Notification Setup Guide

## Overview

BookClick includes a complete email notification system that sends emails for:
- ✅ Booking confirmation (when created)
- ✅ Booking approval
- ✅ Booking rejection
- ✅ Booking cancellation
- ✅ Booking reminders (24h before)
- ✅ Admin notifications (new booking requests)

## Configuration

### 1. Update .env File

Edit your `.env` file with your email settings:

```bash
# For Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@university.edu
```

### 2. Gmail Setup (Recommended for Testing)

#### Option A: App Password (Recommended)
1. Enable 2-Factor Authentication on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this password in `EMAIL_HOST_PASSWORD`

#### Option B: Less Secure Apps (Not Recommended)
1. Go to: https://myaccount.google.com/lesssecureapps
2. Enable "Allow less secure apps"
3. Use your regular password

### 3. Other Email Providers

#### Outlook/Office365
```bash
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

#### Yahoo
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Custom SMTP Server
```bash
EMAIL_HOST=smtp.yourserver.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
```

### 4. Console Backend (For Development)

To test without sending real emails (prints to console):

```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Email Triggers

### Automatic Emails

1. **Booking Created**
   - Sent to: User who created the booking
   - Sent to: All administrators
   - Trigger: When `booking.save()` is called

2. **Booking Approved**
   - Sent to: User who created the booking
   - Trigger: When admin approves booking

3. **Booking Rejected**
   - Sent to: User who created the booking
   - Trigger: When admin rejects booking

4. **Booking Cancelled**
   - Sent to: User who created the booking
   - Trigger: When booking is cancelled

### Manual Reminders

Send reminder emails for bookings happening tomorrow:

```bash
python manage.py send_booking_reminders
```

**Setup Cron Job (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/bookclick && /path/to/venv/bin/python manage.py send_booking_reminders
```

**Setup Task Scheduler (Windows):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `manage.py send_booking_reminders`
7. Start in: `C:\path\to\bookclick`

## Testing Emails

### Test in Django Shell

```python
python manage.py shell

from bookings.emails import send_booking_confirmation_email
from bookings.models import Booking

# Get a booking
booking = Booking.objects.first()

# Send test email
send_booking_confirmation_email(booking)
```

### Test with Management Command

```bash
# Create a test booking first, then:
python manage.py send_booking_reminders
```

## Email Templates

Email content is defined in `bookings/emails.py`. You can customize:

- Subject lines
- Email body text
- Formatting

Example customization:

```python
def send_booking_approval_email(booking):
    subject = f'✅ Booking Approved - {booking.room.name}'
    
    message = f"""
    🎉 Great news, {booking.user.get_full_name()}!
    
    Your booking has been APPROVED!
    
    📍 Room: {booking.room.name}
    🏢 Building: {booking.room.building}
    📅 Date: {booking.date.strftime('%B %d, %Y')}
    ⏰ Time: {booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}
    
    See you there!
    """
    # ... rest of the code
```

## Troubleshooting

### Emails Not Sending

1. **Check .env configuration**
   ```bash
   cat .env | grep EMAIL
   ```

2. **Test SMTP connection**
   ```python
   python manage.py shell
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```

3. **Check Django logs**
   - Look for error messages in console
   - Check if EMAIL_BACKEND is correct

4. **Verify credentials**
   - Make sure email/password are correct
   - For Gmail, use App Password, not regular password

### Common Errors

**"SMTPAuthenticationError"**
- Wrong username/password
- Need to enable "Less secure apps" or use App Password

**"SMTPServerDisconnected"**
- Wrong EMAIL_HOST or EMAIL_PORT
- Firewall blocking connection

**"Connection refused"**
- EMAIL_PORT is wrong
- Server not allowing connections

## Production Recommendations

1. **Use a dedicated email service:**
   - SendGrid
   - Mailgun
   - Amazon SES
   - Postmark

2. **Setup email templates:**
   - Use HTML templates for better formatting
   - Add university logo
   - Include links to booking details

3. **Add email queue:**
   - Use Celery for async email sending
   - Prevents slow page loads
   - Better error handling

4. **Monitor email delivery:**
   - Track sent/failed emails
   - Log email activity
   - Setup alerts for failures

## Email Customization

### Add HTML Templates

Create `templates/emails/booking_confirmation.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #007bff; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Booking Confirmation</h1>
    </div>
    <div class="content">
        <p>Dear {{ booking.user.get_full_name }},</p>
        <p>Your booking has been confirmed!</p>
        <!-- Add more details -->
    </div>
</body>
</html>
```

Then update `emails.py` to use the template:

```python
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_booking_confirmation_email(booking):
    subject = f'Booking Confirmation - {booking.room.name}'
    
    # Render HTML template
    html_content = render_to_string('emails/booking_confirmation.html', {
        'booking': booking
    })
    
    # Create email with HTML
    email = EmailMultiAlternatives(
        subject,
        'Plain text version',  # Fallback
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
```

## Support

For email configuration help:
- Check Django documentation: https://docs.djangoproject.com/en/4.2/topics/email/
- Contact: support@university.edu
