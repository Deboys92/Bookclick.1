from django.urls import path
from .views_frontend import (
    rooms_list_view, room_detail_view, room_create_view,
    room_edit_view, room_delete_view
)

urlpatterns = [
    path('', rooms_list_view, name='rooms_list'),
    path('<int:pk>/', room_detail_view, name='room_detail'),
    path('create/', room_create_view, name='room_create'),
    path('<int:pk>/edit/', room_edit_view, name='room_edit'),
    path('<int:pk>/delete/', room_delete_view, name='room_delete'),
]
