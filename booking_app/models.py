from django.db import models
from django.contrib.auth.models import User

class Theatre(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theatres')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    seats_per_row = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Movie(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    poster = models.ImageField(upload_to='posters/', blank=True)
    show_date = models.DateTimeField()
    total_seats = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.theatre.name}"

    class Meta:
        ordering = ['-show_date']


class Seat(models.Model):
    SEAT_STATUS = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('locked', 'Locked'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1)
    column = models.IntegerField()
    status = models.CharField(max_length=20, choices=SEAT_STATUS, default='available')
    
    class Meta:
        unique_together = ('movie', 'row', 'column')

    def __str__(self):
        return f"{self.movie.title} - Seat {self.row}{self.column}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(Seat, related_name='bookings')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-booking_date']
