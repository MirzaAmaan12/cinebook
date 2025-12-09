# Theatre Booking System - Quick Start Guide

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Run Migrations (if not done already)
```bash
python manage.py migrate
python manage.py makemigrations booking_app
python manage.py migrate booking_app
```

### 3. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Main App:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/

---

## 📋 User Workflows

### As a Regular User:
1. Go to home page and browse movies
2. Click "Sign Up" to create an account
3. Login with your credentials
4. Click "Select Seats" on any movie
5. Click on seats to select (green = selected)
6. Click "Proceed to Checkout"
7. Fill in payment details and confirm
8. View your booking confirmation
9. Check "My Bookings" to see all your tickets

### As a Theatre Owner:
1. Register as a new user
2. Navigate to "Own Theatre" or Dashboard
3. Click "Create Theatre" and fill details:
   - Theatre name
   - Location
   - Number of rows (5-20)
   - Number of columns (5-20)
4. Click "Add Movie" from dashboard
5. Fill movie details:
   - Title, description, genre
   - Duration, price per seat
   - Poster image
   - Show date and time
6. Seats are automatically created based on theatre layout
7. View bookings and revenue on dashboard
8. Edit or delete movies as needed

---

## 🎨 UI Features

- **Modern White Design:** Clean, minimalist interface with dark text on white background
- **Visual Seat Grid:** Interactive seat selection with color coding:
  - White = Available
  - Green = Selected
  - Gray = Already Booked
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Smooth Animations:** Hover effects and transitions
- **Bootstrap 5:** Professional component styling

---

## 🔐 Security Features

- User authentication required for bookings
- CSRF protection on all forms
- Session-based data management
- Password hashing
- Admin login required

---

## 📊 Admin Panel Features

Access at `/admin/` with superuser credentials:

- **Users:** Manage user accounts
- **Theatres:** View and manage theatres
- **Movies:** View and manage movies
- **Seats:** View seat availability
- **Bookings:** Track all bookings and revenue

---

## 🛠️ Customization

### Change App Name
Edit `theatre_booking/settings.py` - Update `INSTALLED_APPS`

### Change Database
Edit `theatre_booking/settings.py` - Update `DATABASES`

### Add Custom Styling
Edit `booking_app/static/css/style.css`

### Modify Colors
Update CSS variables in `style.css`:
```css
:root {
    --primary-color: #000;
    --secondary-color: #fff;
    --text-dark: #333;
}
```

---

## 📦 Project Files

```
theatre_booking/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── setup.bat                    # Windows setup script
├── setup.sh                     # macOS/Linux setup script
├── README.md                    # Full documentation
├── QUICKSTART.md               # This file
├── theatre_booking/            # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── booking_app/                # Main application
    ├── models.py              # Database models
    ├── views.py               # Business logic
    ├── urls.py                # URL routing
    ├── forms.py               # Form definitions
    ├── admin.py               # Admin configuration
    ├── migrations/            # Database migrations
    ├── static/css/            # Stylesheets
    └── templates/             # HTML templates
```

---

## 🐛 Troubleshooting

### Migrations Error
```bash
python manage.py makemigrations
python manage.py migrate
```

### Database Error
```bash
# Reset database (deletes all data)
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

---

## 🌐 Deployment

For production:
1. Set `DEBUG = False` in settings.py
2. Set secure `SECRET_KEY`
3. Configure allowed hosts
4. Use environment variables for sensitive data
5. Set up proper database (PostgreSQL recommended)
6. Configure static files with WhiteNoise or CDN
7. Use Gunicorn as WSGI server
8. Set up Nginx reverse proxy

---

## 📞 Support

For issues or feature requests, check the code comments and documentation within each file.

Enjoy your Theatre Booking System! 🎭
