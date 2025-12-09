from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Movies and Bookings
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/create-booking/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # Owner Dashboard
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/create-theatre/', views.create_theatre, name='create_theatre'),
    path('owner/theatre/<int:theatre_id>/edit-seats/', views.edit_theatre_seats, name='edit_theatre_seats'),
    path('owner/theatre/<int:theatre_id>/create-movie/', views.create_movie, name='create_movie'),
    path('owner/movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('owner/movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
]
