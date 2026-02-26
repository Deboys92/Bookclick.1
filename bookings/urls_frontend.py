from django.urls import path
from .views_frontend import (
    bookings_list_view, booking_detail_view, booking_create_view,
    booking_edit_view, booking_cancel_view, booking_approve_view,
    booking_reject_view, check_availability_view
)

urlpatterns = [
    path('', bookings_list_view, name='bookings_list'),
    path('<int:pk>/', booking_detail_view, name='booking_detail'),
    path('create/', booking_create_view, name='booking_create'),
    path('<int:pk>/edit/', booking_edit_view, name='booking_edit'),
    path('<int:pk>/cancel/', booking_cancel_view, name='booking_cancel'),
    path('<int:pk>/approve/', booking_approve_view, name='booking_approve'),
    path('<int:pk>/reject/', booking_reject_view, name='booking_reject'),
    path('check-availability/', check_availability_view, name='check_availability'),
]
