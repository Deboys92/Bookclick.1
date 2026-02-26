from django.urls import path
from .views_frontend import (
    home, register_view, login_view, logout_view,
    profile_view, dashboard_view, admin_dashboard_view,
    verify_email, resend_verification_email
)


urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
]
