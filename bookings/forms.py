from django import forms
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'room', 'title', 'description', 
            'date', 'end_date', 'start_time', 
            'end_time', 'number_of_attendees'
        ]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().strftime('%Y-%m-%d')
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().strftime('%Y-%m-%d')
                }
            ),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'number_of_attendees': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ end_date optionnel
        self.fields['end_date'].required = False
        
        # Si c'est une nouvelle réservation, définir la date de fin par défaut
        if not self.instance.pk:
            self.initial['end_date'] = self.initial.get('date')
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        end_date = cleaned_data.get('end_date', date)
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        # Si end_date n'est pas défini, utiliser la date de début
        if not end_date:
            end_date = date
            cleaned_data['end_date'] = date
        
        # Vérifier que la date de fin n'est pas avant la date de début
        if end_date and date and end_date < date:
            self.add_error('end_date', 'La date de fin ne peut pas être avant la date de début')
        
        # Vérifier que l'heure de fin est après l'heure de début
        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', 'L\'heure de fin doit être après l\'heure de début')
        
        return cleaned_data
