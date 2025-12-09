from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
import json
import uuid

from .models import Theatre, Movie, Seat, Booking
from .forms import UserRegistrationForm, TheatreForm, MovieForm


def home(request):
    """Home page with available movies"""
    movies = Movie.objects.all().order_by('-show_date')
    theatres = Theatre.objects.all()
    context = {
        'movies': movies,
        'theatres': theatres,
        'page_title': 'Theatre Booking System'
    }
    return render(request, 'booking_app/home.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'booking_app/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'booking_app/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'booking_app/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def movie_detail(request, movie_id):
    """Movie detail with seat selection"""
    movie = get_object_or_404(Movie, id=movie_id)
    seats = movie.seats.all().order_by('row', 'column')

    # If no seats exist, create them now
    if not seats.exists():
        theatre = movie.theatre
        rows = ['A', 'B', 'C', 'D', 'E']
        seats_per_row = theatre.seats_per_row
        for row_letter in rows:
            for col in range(1, seats_per_row + 1):
                Seat.objects.get_or_create(
                    movie=movie,
                    row=row_letter,
                    column=col,
                    defaults={'status': 'available'}
                )
        seats = movie.seats.all().order_by('row', 'column')

    # Uniform layout: all rows have same seat count and alignment
    seat_rows = {row: [] for row in ['A', 'B', 'C', 'D', 'E']}
    for seat in seats:
        seat_rows[seat.row].append(seat)

    # Keep seats aligned across rows
    for row_key, row_seats in seat_rows.items():
        seat_rows[row_key] = sorted(row_seats, key=lambda s: s.column)

    context = {
        'movie': movie,
        'seat_rows': seat_rows,
        'rows': ['A', 'B', 'C', 'D', 'E'],
        'seat_count': movie.theatre.seats_per_row,
    }
    return render(request, 'booking_app/movie_detail.html', context)



@login_required(login_url='login')
def create_booking(request, movie_id):
    """Create booking and redirect to confirmation page"""
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        seat_ids_str = request.POST.get('seat_ids', '')
        seat_ids = [int(sid) for sid in seat_ids_str.split(',') if sid.isdigit()]
        
        if not seat_ids:
            return redirect('movie_detail', movie_id=movie_id)
        
        seats = Seat.objects.filter(id__in=seat_ids, movie=movie, status='available')

        if len(seats) != len(seat_ids):
            # Handle error, some seats might have been booked by someone else
            return render(request, 'booking_app/error.html', {'error': 'Some of the selected seats are no longer available.'})

        total_price = Decimal(len(seats)) * movie.price_per_seat

        try:
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                movie=movie,
                total_price=total_price,
                status='completed',
                transaction_id=f"BK-{uuid.uuid4().hex[:8].upper()}",
            )
            
            # Add seats to booking
            booking.seats.set(seats)
            
            # Mark seats as booked
            seats.update(status='booked')
            
            return redirect('booking_confirmation', booking_id=booking.id)
        except Exception as e:
            return render(request, 'booking_app/error.html', {'error': str(e)})
    
    return redirect('home')


@login_required(login_url='login')
def user_dashboard(request):
    """User dashboard with movies and bookings overview"""
    movies = Movie.objects.all().order_by('show_date')
    bookings = request.user.bookings.select_related('movie', 'movie__theatre').prefetch_related('seats')

    context = {
        'upcoming_movies': movies[:6],
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'upcoming_count': bookings.filter(movie__show_date__gte=timezone.now()).count(),
    }
    return render(request, 'booking_app/user_dashboard.html', context)



@login_required(login_url='login')
def booking_confirmation(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    seats = booking.seats.all().order_by('row', 'column')
    
    context = {
        'booking': booking,
        'seats': seats,
    }
    return render(request, 'booking_app/booking_confirmation.html', context)


@login_required(login_url='login')
def my_bookings(request):
    """User's bookings list"""
    bookings = request.user.bookings.all()
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_app/my_bookings.html', context)


@login_required(login_url='login')
def owner_dashboard(request):
    """Theatre owner dashboard"""
    if not request.user.theatres.exists():
        return redirect('create_theatre')
    
    theatres = request.user.theatres.all()
    movies = Movie.objects.filter(theatre__in=theatres)
    bookings = Booking.objects.filter(movie__in=movies)
    
    context = {
        'theatres': theatres,
        'movies': movies,
        'bookings': bookings,
        'total_revenue': sum(b.total_price for b in bookings if b.status == 'completed'),
        'total_bookings': bookings.count(),
    }
    return render(request, 'booking_app/owner_dashboard.html', context)


@login_required(login_url='login')
def create_theatre(request):
    """Create theatre"""
    if request.method == 'POST':
        form = TheatreForm(request.POST)
        if form.is_valid():
            theatre = form.save(commit=False)
            theatre.owner = request.user
            theatre.save()
            return redirect('owner_dashboard')
    else:
        form = TheatreForm()
    
    return render(request, 'booking_app/create_theatre.html', {'form': form})


@login_required(login_url='login')
def edit_theatre_seats(request, theatre_id):
    """Edit theatre seat configuration"""
    return redirect('owner_dashboard')


@login_required(login_url='login')
def create_movie(request, theatre_id):
    """Create movie"""
    theatre = get_object_or_404(Theatre, id=theatre_id, owner=request.user)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.theatre = theatre
            movie.total_seats = 5 * theatre.seats_per_row
            movie.save()
            
            # Create seats based on theatre configuration
            rows = ['A', 'B', 'C', 'D', 'E']
            seats_per_row = theatre.seats_per_row

            for row_letter in rows:
                for col in range(1, seats_per_row + 1):
                    Seat.objects.get_or_create(
                        movie=movie,
                        row=row_letter,
                        column=col,
                        defaults={'status': 'available'}
                    )
            
            return redirect('owner_dashboard')
    else:
        form = MovieForm()
    
    return render(request, 'booking_app/create_movie.html', {'form': form, 'theatre': theatre})


@login_required(login_url='login')
def edit_movie(request, movie_id):
    """Edit movie"""
    movie = get_object_or_404(Movie, id=movie_id, theatre__owner=request.user)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'booking_app/edit_movie.html', {'form': form, 'movie': movie})


@login_required(login_url='login')
def delete_movie(request, movie_id):
    """Delete movie"""
    movie = get_object_or_404(Movie, id=movie_id, theatre__owner=request.user)
    
    if request.method == 'POST':
        movie.delete()
        return redirect('owner_dashboard')
    
    return render(request, 'booking_app/delete_movie.html', {'movie': movie})
