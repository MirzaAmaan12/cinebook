from django import forms
from django.contrib.auth.models import User
from .models import Theatre, Movie, Seat, Booking

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class TheatreForm(forms.ModelForm):
    class Meta:
        model = Theatre
        fields = ['name', 'location', 'seats_per_row']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Theatre Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'seats_per_row': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '30', 'value': '10'}),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'duration', 'price_per_seat', 'poster', 'show_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (minutes)'}),
            'price_per_seat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Price per Seat'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'show_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Create seats for the movie based on theatre configuration
            theatre = instance.theatre
            rows = ['A', 'B', 'C', 'D', 'E']
            seats_per_row = theatre.seats_per_row
            
            for row_letter in rows:
                for col in range(1, seats_per_row + 1):
                    Seat.objects.get_or_create(
                        movie=instance,
                        row=row_letter,
                        column=col
                    )
        return instance
