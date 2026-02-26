from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'get_date_range', 'get_time_range', 'status', 'created_at']
    list_filter = ['status', 'date', 'room__building']
    search_fields = ['title', 'user__email', 'room__name', 'description']
    ordering = ['-date', '-start_time']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Informations de réservation', {
            'fields': ('user', 'room', 'title', 'description', 'number_of_attendees')
        }),
        ('Planning', {
            'fields': ('date', 'end_date', 'start_time', 'end_time')
        }),
        ('Statut et approbation', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_bookings', 'reject_bookings', 'cancel_bookings']
    
    def get_date_range(self, obj):
        if obj.end_date and obj.end_date != obj.date:
            return format_html(
                '<span title="Du {} au {}">{} - {}</span>',
                obj.date.strftime('%d/%m/%Y'),
                obj.end_date.strftime('%d/%m/%Y'),
                obj.date.strftime('%d/%m/%Y'),
                obj.end_date.strftime('%d/%m/%Y')
            )
        return obj.date.strftime('%d/%m/%Y')
    get_date_range.short_description = 'Période'
    get_date_range.admin_order_field = 'date'
    
    def get_time_range(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
    get_time_range.short_description = 'Heures'
    get_time_range.admin_order_field = 'start_time'
    
    def approve_bookings(self, request, queryset):
        count = 0
        for booking in queryset:
            if booking.status == 'PENDING':
                booking.approve(request.user)
                count += 1
        self.message_user(request, f'{count} réservation(s) approuvée(s) avec succès.')
    approve_bookings.short_description = 'Approuver les réservations sélectionnées'
    
    def reject_bookings(self, request, queryset):
        count = 0
        for booking in queryset:
            if booking.status == 'PENDING':
                booking.reject(request.user, reason='Rejetée par l\'administrateur')
                count += 1
        self.message_user(request, f'{count} réservation(s) rejetée(s).')
    reject_bookings.short_description = 'Rejeter les réservations sélectionnées'
    
    def cancel_bookings(self, request, queryset):
        count = 0
        for booking in queryset:
            if booking.status in ['PENDING', 'APPROVED']:
                booking.cancel()
                count += 1
        self.message_user(request, f'{count} réservation(s) annulée(s).')
    cancel_bookings.short_description = 'Annuler les réservations sélectionnées'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filtrer pour ne montrer que les réservations futures ou récentes (30 derniers jours)
        thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
        return qs.filter(date__gte=thirty_days_ago).select_related('user', 'room', 'approved_by')
