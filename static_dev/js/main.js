// BookClick Main JavaScript

// Auto-hide alerts after 5 seconds
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Format date inputs to today's date
function setMinDate() {
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.hasAttribute('min')) {
            input.setAttribute('min', today);
        }
    });
}

// Check availability before booking
function checkAvailability(roomId, date, startTime, endTime) {
    if (!roomId || !date || !startTime || !endTime) {
        alert('Please fill in all fields');
        return false;
    }
    
    // Show loading
    showLoading();
    
    // Make AJAX request
    $.ajax({
        url: '/api/bookings/check_availability/',
        method: 'GET',
        data: {
            room_id: roomId,
            date: date,
            start_time: startTime,
            end_time: endTime
        },
        success: function(response) {
            hideLoading();
            if (response.available) {
                alert('Room is available!');
            } else {
                alert('Room is not available at this time. Please choose another time slot.');
            }
        },
        error: function() {
            hideLoading();
            alert('Error checking availability. Please try again.');
        }
    });
}

// Show loading overlay
function showLoading() {
    const overlay = $('<div class="spinner-overlay"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>');
    $('body').append(overlay);
}

// Hide loading overlay
function hideLoading() {
    $('.spinner-overlay').remove();
}

// Filter rooms
function filterRooms() {
    const searchTerm = $('#searchInput').val().toLowerCase();
    const roomType = $('#roomTypeFilter').val();
    const building = $('#buildingFilter').val();
    
    $('.room-card').each(function() {
        const card = $(this);
        const name = card.find('.card-title').text().toLowerCase();
        const type = card.data('type');
        const bldg = card.data('building');
        
        let show = true;
        
        if (searchTerm && !name.includes(searchTerm)) {
            show = false;
        }
        
        if (roomType && type !== roomType) {
            show = false;
        }
        
        if (building && bldg !== building) {
            show = false;
        }
        
        if (show) {
            card.parent().show();
        } else {
            card.parent().hide();
        }
    });
}

// Validate booking form
function validateBookingForm() {
    const startTime = $('#id_start_time').val();
    const endTime = $('#id_end_time').val();
    
    if (startTime && endTime) {
        if (endTime <= startTime) {
            alert('End time must be after start time!');
            return false;
        }
    }
    
    return true;
}

// Initialize tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// Initialize popovers
$(function () {
    $('[data-toggle="popover"]').popover();
});

// Room capacity warning
function checkCapacity(roomCapacity) {
    const attendees = $('#id_number_of_attendees').val();
    if (attendees && roomCapacity) {
        if (parseInt(attendees) > parseInt(roomCapacity)) {
            $('#capacityWarning').show();
            return false;
        } else {
            $('#capacityWarning').hide();
            return true;
        }
    }
    return true;
}

// Real-time search
let searchTimeout;
$('#searchInput').on('keyup', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(filterRooms, 300);
});

// Date picker initialization
$(document).ready(function() {
    setMinDate();
});

// Print booking details
function printBooking() {
    window.print();
}

// Export to calendar
function exportToCalendar(title, date, startTime, endTime, location) {
    // Create ICS file content
    const icsContent = `BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:${title}
DTSTART:${date}T${startTime.replace(':', '')}00
DTEND:${date}T${endTime.replace(':', '')}00
LOCATION:${location}
END:VEVENT
END:VCALENDAR`;
    
    // Create download link
    const blob = new Blob([icsContent], { type: 'text/calendar' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'booking.ics';
    link.click();
}

// Booking form validation on submit
$('#bookingForm').on('submit', function(e) {
    if (!validateBookingForm()) {
        e.preventDefault();
        return false;
    }
});

// Equipment filter checkboxes
$('.equipment-filter').on('change', function() {
    filterRooms();
});

// Smooth scroll to top
$('.scroll-to-top').on('click', function() {
    $('html, body').animate({ scrollTop: 0 }, 'smooth');
});

// Add scroll to top button
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('.scroll-to-top').fadeIn();
    } else {
        $('.scroll-to-top').fadeOut();
    }
});

// Mobile menu toggle
$('.navbar-toggler').on('click', function() {
    $(this).toggleClass('active');
});

// Form field auto-focus
$('form').each(function() {
    $(this).find('input:not([type="hidden"]):first').focus();
});

// Prevent double form submission
$('form').on('submit', function() {
    $(this).find('button[type="submit"]').prop('disabled', true);
    setTimeout(function() {
        $('button[type="submit"]').prop('disabled', false);
    }, 3000);
});

console.log('BookClick initialized successfully!');
