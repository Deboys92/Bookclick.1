from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User
from rooms.models import Room
from bookings.models import Booking


def home(request):
    """Home page view"""
    context = {}
    
    if request.user.is_authenticated:
        # Get stats for authenticated users
        context['total_rooms'] = Room.objects.count()
        context['available_rooms'] = Room.objects.filter(status='AVAILABLE').count()
        context['my_bookings'] = Booking.objects.filter(user=request.user).count()
        context['upcoming_bookings'] = Booking.objects.filter(
            user=request.user,
            date__gte=timezone.now().date(),
            status__in=['PENDING', 'APPROVED']
        ).count()
    
    return render(request, 'home.html', context)


def send_verification_email(user, request):
    """Send verification email to the user"""
    print(f"Sending verification email to {user.email}")  # Debug print
    token = default_token_generator.make_token(user)
    uid = user.pk
    uidb64 = urlsafe_base64_encode(force_bytes(uid))
    domain = request.get_host()
    
    subject = 'Verify your BookClick account'
    html_message = render_to_string('emails/account_verification_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'uidb64': uidb64,
        'token': token,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

def verify_email(request, uidb64, token):
    """Verify user's email address"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_verified = True
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.success(request, 'Your email has been verified! You can now log in.')
        else:
            messages.error(request, 'Invalid verification link.')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
    
    return redirect('login')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        print("POST request received")  # Debug
        # Get form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        student_id = request.POST.get('student_id')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        
        print(f"Form data: email={email}, username={username}")  # Debug
        
        # Validate passwords match
        if password != password_confirm:
            print("Passwords don't match")  # Debug
            messages.error(request, 'Passwords do not match!')
            return render(request, 'registration/register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            print("Email already exists")  # Debug
            messages.error(request, 'Email already registered!')
            return render(request, 'registration/register.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            print("Username already exists")  # Debug
            messages.error(request, 'Username already taken!')
            return render(request, 'registration/register.html')
        
        print("Creating user...")  # Debug
        try:
            # Create the user (initially inactive)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                student_id=student_id,
                phone_number=phone_number,
                department=department,
                is_active=False  # User will be activated after email verification
            )
            print(f"User created: {user.username}, {user.email}")  # Debug
            
            # Send verification email
            print("About to send verification email")  # Debug
            try:
                send_verification_email(user, request)
                print("Verification email sent successfully")  # Debug
                messages.success(request, 'Registration successful! Please check your email to verify your account.')
                return redirect('login')
            except Exception as e:
                print(f"Error sending verification email: {e}")  # Debug
                user.delete()  # Clean up if email sending fails
                messages.error(request, 'Failed to send verification email. Please try again.')
        except Exception as e:
            print(f"Error creating user: {e}")  # Debug
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'registration/register.html')
    
    return render(request, 'registration/register.html')


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')  # This is actually email
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid email or password!')
    
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        # Update profile
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.department = request.POST.get('department', user.department)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def dashboard_view(request):
    """User dashboard view"""
    user = request.user
    
    # Get user's bookings
    my_bookings = Booking.objects.filter(user=user).order_by('-date', '-start_time')[:5]
    
    # Get upcoming bookings
    upcoming = Booking.objects.filter(
        user=user,
        date__gte=timezone.now().date(),
        status__in=['PENDING', 'APPROVED']
    ).order_by('date', 'start_time')
    
    # Get statistics
    total_bookings = Booking.objects.filter(user=user).count()
    pending_bookings = Booking.objects.filter(user=user, status='PENDING').count()
    approved_bookings = Booking.objects.filter(user=user, status='APPROVED').count()
    
    context = {
        'my_bookings': my_bookings,
        'upcoming': upcoming,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    """Admin dashboard view"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('dashboard')
    
    # Get statistics
    total_users = User.objects.count()
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    
    # Get recent bookings
    recent_bookings = Booking.objects.select_related('user', 'room').order_by('-created_at')[:10]
    
    # Get pending bookings for approval
    pending_list = Booking.objects.filter(status='PENDING').select_related('user', 'room')
    
    # Room utilization stats
    room_stats = Room.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]
    
    context = {
        'total_users': total_users,
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'recent_bookings': recent_bookings,
        'pending_list': pending_list,
        'room_stats': room_stats,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


def resend_verification_email(request):
    """Resend verification email to the user"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, 'This account is already verified. Please log in.')
                return redirect('login')
            
            # Send verification email
            send_verification_email(user, request)
            messages.success(request, 'A new verification email has been sent. Please check your inbox.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('resend-verification')
    
    return render(request, 'registration/resend_verification.html')