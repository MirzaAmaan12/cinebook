from django.contrib import admin
from .models import Theatre, Movie, Seat, Booking

@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    # 'total_seats' is a field on Movie, not Theatre. Remove to pass system checks.
    list_display = ['name', 'location', 'owner', 'created_at']
    search_fields = ['name', 'location']
    list_filter = ['created_at']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'theatre', 'show_date', 'price_per_seat', 'total_seats']
    search_fields = ['title', 'theatre__name']
    list_filter = ['show_date', 'theatre']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['movie', 'row', 'column', 'status']
    list_filter = ['status', 'movie']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'movie', 'total_price', 'status', 'booking_date']
    search_fields = ['user__username', 'movie__title']
    list_filter = ['status', 'booking_date']
