from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Room


@login_required
def rooms_list_view(request):
    """List all rooms with filters"""
    rooms = Room.objects.all()
    
    # Apply filters
    room_type = request.GET.get('room_type')
    building = request.GET.get('building')
    min_capacity = request.GET.get('min_capacity')
    search = request.GET.get('search')
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    if building:
        rooms = rooms.filter(building=building)
    
    if min_capacity:
        try:
            rooms = rooms.filter(capacity__gte=int(min_capacity))
        except ValueError:
            pass
    
    if search:
        rooms = rooms.filter(
            Q(name__icontains=search) |
            Q(building__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Equipment filters
    if request.GET.get('has_projector'):
        rooms = rooms.filter(has_projector=True)
    if request.GET.get('has_wifi'):
        rooms = rooms.filter(has_wifi=True)
    if request.GET.get('has_computer'):
        rooms = rooms.filter(has_computer=True)
    if request.GET.get('has_ac'):
        rooms = rooms.filter(has_ac=True)
    
    # Get unique buildings for filter dropdown
    buildings = Room.objects.values_list('building', flat=True).distinct()
    
    context = {
        'rooms': rooms,
        'buildings': buildings,
        'room_types': Room.ROOM_TYPE_CHOICES,
    }
    
    return render(request, 'rooms/rooms_list.html', context)


@login_required
def room_detail_view(request, pk):
    """View room details"""
    room = get_object_or_404(Room, pk=pk)
    
    # Get upcoming bookings for this room
    from bookings.models import Booking
    from django.utils import timezone
    
    upcoming_bookings = Booking.objects.filter(
        room=room,
        date__gte=timezone.now().date(),
        status__in=['PENDING', 'APPROVED']
    ).order_by('date', 'start_time')[:10]
    
    context = {
        'room': room,
        'upcoming_bookings': upcoming_bookings,
    }
    
    return render(request, 'rooms/room_detail.html', context)


@login_required
def room_create_view(request):
    """Create new room (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('rooms_list')
    
    if request.method == 'POST':
        try:
            room = Room.objects.create(
                name=request.POST.get('name'),
                room_type=request.POST.get('room_type'),
                building=request.POST.get('building'),
                floor=request.POST.get('floor'),
                capacity=request.POST.get('capacity'),
                description=request.POST.get('description'),
                status=request.POST.get('status', 'AVAILABLE'),
                has_projector=request.POST.get('has_projector') == 'on',
                has_whiteboard=request.POST.get('has_whiteboard') == 'on',
                has_computer=request.POST.get('has_computer') == 'on',
                has_wifi=request.POST.get('has_wifi') == 'on',
                has_ac=request.POST.get('has_ac') == 'on',
                has_audio_system=request.POST.get('has_audio_system') == 'on',
            )
            
            if 'image' in request.FILES:
                room.image = request.FILES['image']
                room.save()
            
            messages.success(request, f'Room "{room.name}" created successfully!')
            return redirect('room_detail', pk=room.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating room: {str(e)}')
    
    return render(request, 'rooms/room_form.html', {
        'room_types': Room.ROOM_TYPE_CHOICES,
        'status_choices': Room.STATUS_CHOICES,
    })


@login_required
def room_edit_view(request, pk):
    """Edit room (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('rooms_list')
    
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        try:
            room.name = request.POST.get('name')
            room.room_type = request.POST.get('room_type')
            room.building = request.POST.get('building')
            room.floor = request.POST.get('floor')
            room.capacity = request.POST.get('capacity')
            room.description = request.POST.get('description')
            room.status = request.POST.get('status')
            room.has_projector = request.POST.get('has_projector') == 'on'
            room.has_whiteboard = request.POST.get('has_whiteboard') == 'on'
            room.has_computer = request.POST.get('has_computer') == 'on'
            room.has_wifi = request.POST.get('has_wifi') == 'on'
            room.has_ac = request.POST.get('has_ac') == 'on'
            room.has_audio_system = request.POST.get('has_audio_system') == 'on'
            
            if 'image' in request.FILES:
                room.image = request.FILES['image']
            
            room.save()
            messages.success(request, f'Room "{room.name}" updated successfully!')
            return redirect('room_detail', pk=room.pk)
            
        except Exception as e:
            messages.error(request, f'Error updating room: {str(e)}')
    
    context = {
        'room': room,
        'room_types': Room.ROOM_TYPE_CHOICES,
        'status_choices': Room.STATUS_CHOICES,
        'is_edit': True,
    }
    
    return render(request, 'rooms/room_form.html', context)


@login_required
def room_delete_view(request, pk):
    """Delete room (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('rooms_list')
    
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        room_name = room.name
        room.delete()
        messages.success(request, f'Room "{room_name}" deleted successfully!')
        return redirect('rooms_list')
    
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})
