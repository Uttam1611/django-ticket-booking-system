# Ticket Booking System

A web-based Ticket Booking System built with Django.  
This project supports user and admin roles, slot management, booking, and cancellation features.

## Features

- User registration and login (with profile photo upload)
- Admin registration and login
- User dashboard: book slots, view/cancel bookings
- Admin dashboard: manage slots, view all bookings
- Slot availability management
- Custom 404 error page
- Automated tests for core features

## Tech Stack

- Python 3.11+
- Django 4.2+
- Bootstrap 5 (for UI)
- SQLite (default, can be changed)

## Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/Uttam1611/django-ticket-booking-system
cd ticket-booking-system
```

### 2. Create and activate a virtual environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Apply migrations

```sh
python manage.py migrate
```

### 5. Create a superuser (for Django admin)

```sh
python manage.py createsuperuser
```

### 6. Run the development server

```sh
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Running Tests

To run all automated tests:

```sh
python manage.py test
```

---

## Project Structure

```
ticket_booking/
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   ├── tests.py
│   └── views.py
├── bookings/
│   ├── migrations/
│   ├── templates/bookings/
│   ├── tests.py
│   └── views.py
├── ticket_booking/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
├── manage.py
└── requirements.txt
```

---

## Environment Variables

- `SECRET_KEY` (set in `settings.py` for production)
- `DEBUG` (set to `False` in production)
- Database settings (default is SQLite)

---

## License

This project is licensed under the MIT License.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

