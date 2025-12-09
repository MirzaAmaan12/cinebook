"""
Sample data population script for testing
Run: python manage.py shell < populate_sample_data.py
"""

from django.contrib.auth.models import User
from booking_app.models import Theatre, Movie
from datetime import datetime, timedelta
from decimal import Decimal

# Create test users
print("Creating test users...")

# Regular users
user1, created = User.objects.get_or_create(
    username='john_doe',
    defaults={
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)
if created:
    user1.set_password('password123')
    user1.save()
    print("Created user: john_doe")

user2, created = User.objects.get_or_create(
    username='jane_smith',
    defaults={
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith'
    }
)
if created:
    user2.set_password('password123')
    user2.save()
    print("Created user: jane_smith")

# Theatre owner
owner1, created = User.objects.get_or_create(
    username='theatre_owner1',
    defaults={
        'email': 'owner@example.com',
        'first_name': 'Theatre',
        'last_name': 'Owner'
    }
)
if created:
    owner1.set_password('owner123')
    owner1.save()
    print("Created owner: theatre_owner1")

# Create theatres
print("\nCreating theatres...")

theatre1, created = Theatre.objects.get_or_create(
    name='Galaxy Cinemas',
    owner=owner1,
    defaults={
        'location': '123 Main Street, Downtown',
        'rows': 10,
        'columns': 15,
        'total_seats': 150
    }
)
if created:
    print(f"Created theatre: {theatre1.name}")

theatre2, created = Theatre.objects.get_or_create(
    name='Star Plaza Multiplex',
    owner=owner1,
    defaults={
        'location': '456 Park Avenue, Uptown',
        'rows': 12,
        'columns': 18,
        'total_seats': 216
    }
)
if created:
    print(f"Created theatre: {theatre2.name}")

# Create movies
print("\nCreating movies...")

now = datetime.now()

movie1, created = Movie.objects.get_or_create(
    title='The Last Hope',
    theatre=theatre1,
    defaults={
        'description': 'An epic sci-fi adventure that will take you to the edge of the universe.',
        'genre': 'Sci-Fi',
        'duration': 148,
        'price_per_seat': Decimal('250.00'),
        'show_date': now + timedelta(days=3),
        'total_seats': theatre1.total_seats
    }
)
if created:
    print(f"Created movie: {movie1.title}")
    # Create seats
    from string import ascii_uppercase
    for row in range(theatre1.rows):
        for col in range(theatre1.columns):
            from booking_app.models import Seat
            Seat.objects.get_or_create(
                movie=movie1,
                row=ascii_uppercase[row],
                column=col + 1,
                defaults={'status': 'available'}
            )
    print(f"  - Created {theatre1.total_seats} seats")

movie2, created = Movie.objects.get_or_create(
    title='Love in Paris',
    theatre=theatre1,
    defaults={
        'description': 'A romantic drama set in the beautiful streets of Paris.',
        'genre': 'Romance',
        'duration': 124,
        'price_per_seat': Decimal('200.00'),
        'show_date': now + timedelta(days=5),
        'total_seats': theatre1.total_seats
    }
)
if created:
    print(f"Created movie: {movie2.title}")
    # Create seats
    from string import ascii_uppercase
    for row in range(theatre1.rows):
        for col in range(theatre1.columns):
            from booking_app.models import Seat
            Seat.objects.get_or_create(
                movie=movie2,
                row=ascii_uppercase[row],
                column=col + 1,
                defaults={'status': 'available'}
            )
    print(f"  - Created {theatre1.total_seats} seats")

movie3, created = Movie.objects.get_or_create(
    title='Action Heroes',
    theatre=theatre2,
    defaults={
        'description': 'Non-stop action and thrilling stunts in this blockbuster.',
        'genre': 'Action',
        'duration': 156,
        'price_per_seat': Decimal('300.00'),
        'show_date': now + timedelta(days=2),
        'total_seats': theatre2.total_seats
    }
)
if created:
    print(f"Created movie: {movie3.title}")
    # Create seats
    from string import ascii_uppercase
    for row in range(theatre2.rows):
        for col in range(theatre2.columns):
            from booking_app.models import Seat
            Seat.objects.get_or_create(
                movie=movie3,
                row=ascii_uppercase[row],
                column=col + 1,
                defaults={'status': 'available'}
            )
    print(f"  - Created {theatre2.total_seats} seats")

print("\n✅ Sample data created successfully!")
print("\nTest Accounts:")
print("  Regular User: john_doe / password123")
print("  Regular User: jane_smith / password123")
print("  Theatre Owner: theatre_owner1 / owner123")
