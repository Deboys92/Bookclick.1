from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from .models import Booking
from .forms import BookingForm
from rooms.models import Room


@login_required
def bookings_list_view(request):
    """List all bookings"""
    user = request.user
    
    # Filter bookings based on user role
    if user.is_admin():
        bookings = Booking.objects.all()
    else:
        # Non-admins see their own bookings and approved bookings
        bookings = Booking.objects.filter(
            Q(user=user) | Q(status='APPROVED')
        )
    
    bookings = bookings.select_related('user', 'room').order_by('-date', '-start_time')
    
    # Apply filters
    status_filter = request.GET.get('status')
    room_filter = request.GET.get('room')
    date_filter = request.GET.get('date')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if room_filter:
        bookings = bookings.filter(room_id=room_filter)
    
    if date_filter:
        bookings = bookings.filter(date=date_filter)
    
    # Show only upcoming by default
    if request.GET.get('show_all') != 'true':
        bookings = bookings.filter(date__gte=timezone.now().date())
    
    context = {
        'bookings': bookings,
        'rooms': Room.objects.all(),
        'status_choices': Booking.STATUS_CHOICES,
    }
    
    return render(request, 'bookings/bookings_list.html', context)


@login_required
def booking_detail_view(request, pk):
    """View booking details"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    if not request.user.is_admin() and booking.user != request.user and booking.status != 'APPROVED':
        messages.error(request, 'Access denied!')
        return redirect('bookings_list')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def booking_create_view(request):
    """Create new booking"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                
                # Si end_date n'est pas défini, utiliser la date de début
                if not booking.end_date:
                    booking.end_date = booking.date
                
                booking.save()
                
                # Envoyer les emails de confirmation
                try:
                    from .emails import send_booking_confirmation_email, send_admin_notification_email
                    send_booking_confirmation_email(booking)
                    send_admin_notification_email(booking)
                except Exception as e:
                    print(f"Erreur lors de l'envoi des emails: {e}")
                
                messages.success(request, 'Réservation créée avec succès ! En attente de validation.')
                return redirect('booking_detail', pk=booking.pk)
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la création de la réservation : {str(e)}')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = BookingForm()
        
        # Pré-remplir le formulaire avec les paramètres GET si présents
        room_id = request.GET.get('room')
        if room_id:
            form.fields['room'].initial = room_id
        
        date_param = request.GET.get('date')
        if date_param:
            try:
                form.fields['date'].initial = datetime.strptime(date_param, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                pass
    
    context = {
        'form': form,
        'rooms': Room.objects.filter(status='AVAILABLE'),
    }
    
    return render(request, 'bookings/booking_form.html', context)


@login_required
def booking_edit_view(request, pk):
    """Edit booking"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Vérifier si l'utilisateur a le droit de modifier
    if not request.user.is_admin() and booking.user != request.user:
        messages.error(request, 'Vous ne pouvez modifier que vos propres réservations.')
        return redirect('bookings_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                
                # Si end_date n'est pas défini, utiliser la date de début
                if not booking.end_date:
                    booking.end_date = booking.date
                
                # Réinitialiser le statut si un admin modifie
                if request.user.is_admin() and booking.status != 'REJECTED':
                    booking.status = 'PENDING'
                    booking.approved_by = None
                    booking.approval_date = None
                
                booking.save()
                
                messages.success(request, 'Réservation mise à jour avec succès !')
                return redirect('booking_detail', pk=booking.pk)
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la mise à jour de la réservation : {str(e)}')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = BookingForm(instance=booking)
    
    context = {
        'form': form,
        'booking': booking,
        'is_editing': True,
    }
    
    return render(request, 'bookings/booking_form.html', context)


@login_required
def booking_cancel_view(request, pk):
    """Cancel booking"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Only the booking owner or admin can cancel
    if booking.user != request.user and not request.user.is_admin():
        messages.error(request, 'Access denied!')
        return redirect('bookings_list')
    
    if request.method == 'POST':
        booking.cancel()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('bookings_list')
    
    return render(request, 'bookings/booking_confirm_cancel.html', {'booking': booking})


@login_required
def booking_approve_view(request, pk):
    """Approve booking (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('bookings_list')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        booking.approve(request.user)
        messages.success(request, f'Booking approved for {booking.user.get_full_name()}!')
        return redirect('booking_detail', pk=pk)
    
    return render(request, 'bookings/booking_confirm_approve.html', {'booking': booking})


@login_required
def booking_reject_view(request, pk):
    """Reject booking (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('bookings_list')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided')
        booking.reject(request.user, reason)
        messages.success(request, f'Booking rejected!')
        return redirect('booking_detail', pk=pk)
    
    return render(request, 'bookings/booking_confirm_reject.html', {'booking': booking})


@login_required
def check_availability_view(request):
    """Vérifier la disponibilité d'une salle"""
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', start_date)  # Si end_date n'est pas fourni, utiliser start_date
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        try:
            room = Room.objects.get(pk=room_id)
            
            # Convertir les dates en objets date
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                
                # Vérifier que la date de fin n'est pas avant la date de début
                if end_date < start_date:
                    end_date = start_date
                
                # Créer une plage de dates à vérifier
                date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
                
                # Vérifier les chevauchements pour chaque jour
                conflicts = []
                for day in date_range:
                    overlapping = Booking.objects.filter(
                        room=room,
                        date=day,
                        status__in=['PENDING', 'APPROVED']
                    ).exclude(
                        Q(end_time__lte=start_time_str) | Q(start_time__gte=end_time_str)
                    )
                    
                    for booking in overlapping:
                        conflicts.append({
                            'date': day,
                            'booking': booking
                        })
                
                context = {
                    'available': len(conflicts) == 0,
                    'room': room,
                    'start_date': start_date,
                    'end_date': end_date,
                    'start_time': start_time_str,
                    'end_time': end_time_str,
                    'conflicts': conflicts,
                }
                
                return render(request, 'bookings/availability_result.html', context)
                
            except ValueError:
                messages.error(request, 'Format de date invalide')
                return redirect('check_availability')
                
        except Room.DoesNotExist:
            messages.error(request, 'Salle introuvable !')
            return redirect('rooms_list')
    
    # GET request - afficher le formulaire
    room_id = request.GET.get('room')
    selected_room = None
    if room_id:
        selected_room = get_object_or_404(Room, pk=room_id)
    
    context = {
        'rooms': Room.objects.filter(status='AVAILABLE'),
        'selected_room': selected_room,
    }
    
    return render(request, 'bookings/check_availability.html', context)
