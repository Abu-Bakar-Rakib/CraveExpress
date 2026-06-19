# CraveExpress

A modern Django-based food delivery platform with comprehensive features for restaurant management, customer ordering, and real-time delivery tracking. The application includes role-based dashboards for administrators, customers, and delivery personnel.

## Overview

CraveExpress is a full-stack web application built with Django and Django REST Framework, designed to streamline the food delivery experience. It provides a seamless platform for browsing restaurants, managing orders, tracking deliveries, and processing payments.

## Key Features

- **Restaurant Management**: Browse, search, and view detailed restaurant information
- **Menu Management**: Complete menu item catalog with descriptions and pricing
- **Shopping Cart & Checkout**: Intuitive cart management and secure checkout process
- **Order Management**: Real-time order tracking and status updates
- **User Authentication**: Secure login with phone verification capabilities
- **Role-Based Access Control**: 
  - Customer Dashboard: Order history, tracking, and account management
  - Delivery Personnel Dashboard: Active deliveries and route optimization
  - Admin Dashboard: Restaurant and order management, analytics
- **Payment Integration**: Basic payment gateway integration for order processing
- **Media Management**: Efficient image storage for restaurants and products

## System Requirements

- **Python**: 3.10 or higher
- **Database**: SQLite (included, no additional setup required)
- **Operating System**: Windows, macOS, or Linux
- **Package Manager**: pip (included with Python)

All Python dependencies are specified in `requirements.txt` and include Django 5.2.x, Django REST Framework, SimpleJWT, Pillow, NumPy, and Shapely.

## Installation & Setup

### Prerequisites
Ensure Python 3.10+ is installed on your system.

### Step-by-Step Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Abu-Bakar-Rakib/CraveExpress.git
   cd CraveExpress
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   .\venv\Scripts\Activate.ps1
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   ```
   > **Note**: On Windows, if you encounter an execution policy error, run:
   > ```powershell
   > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   > ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   ```bash
   # Apply migrations
   python manage.py migrate
   
   # Create superuser account
   python manage.py createsuperuser
   ```

5. **Load Demo Data (Optional)**
   ```bash
   python manage.py seed_demo
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Application: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
CraveExpress/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # Local SQLite database
├── cravelexpress/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── main/                        # Core application
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── urls.py                 # URL routing
│   ├── serializers.py          # DRF serializers
│   └── management/
│       └── commands/           # Custom management commands
├── templates/                   # HTML templates
│   ├── auth/                   # Authentication pages
│   ├── restaurant/             # Restaurant pages
│   ├── cart/                   # Shopping cart
│   ├── checkout/               # Checkout process
│   ├── customer/               # Customer dashboard
│   ├── delivery/               # Delivery dashboard
│   └── admin/                  # Admin dashboard
├── static/                      # CSS, JavaScript, and static assets
├── media/                       # User-uploaded content
└── venv/                        # Virtual environment (local only)
```

## Common Commands

### Database Management
```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test main

# Run with verbose output
python manage.py test --verbosity=2
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Clear static files
python manage.py collectstatic --clear
```

### Utilities
```bash
# Create new Django app
python manage.py startapp app_name

# Load demo data
python manage.py seed_demo

# Interactive Python shell
python manage.py shell
```

## Configuration

### Environment Settings

The application uses `cravelexpress/settings.py` as the default settings module. Key configuration options:

| Environment Variable | Purpose | Default |
|---|---|---|
| `DEBUG` | Debug mode (development only) | `True` |
| `SECRET_KEY` | Django secret key (set for production) | Configured in settings |
| `ALLOWED_HOSTS` | Allowed hostnames | `127.0.0.1,localhost` |

### Using Environment Variables

To use a `.env` file for configuration:
1. Install `python-dotenv`: `pip install python-dotenv`
2. Create a `.env` file in the project root
3. Load it in your settings or application startup

### Production Deployment

For production deployment:
- Set `DEBUG = False`
- Configure a strong `SECRET_KEY`
- Use a production-grade database (PostgreSQL recommended)
- Configure appropriate `ALLOWED_HOSTS`
- Collect static files: `python manage.py collectstatic`

## Media & Assets

- **User Uploads**: Images are stored in `media/` directory
- **Static Files**: CSS, JavaScript, and static assets in `static/` directory
- **Demo Content**: Available through `python manage.py seed_demo` command

## Troubleshooting

### Windows-Specific Issues

| Issue | Solution |
|---|---|
| Execution Policy Error | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| SQLite Database Locked | Ensure no other processes are using `db.sqlite3`, then retry operations |
| Pillow Installation Issues | Use Python 3.10+ and ensure virtual environment is active |
| Shapely/NumPy Installation Slow | Upgrade pip: `python -m pip install --upgrade pip` |
| Migrations Not Applied | Run `python manage.py makemigrations` followed by `python manage.py migrate` |

### General Troubleshooting

- **Port Already in Use**: Run server on different port: `python manage.py runserver 8001`
- **Module Not Found**: Verify virtual environment is activated and dependencies installed
- **Database Migration Errors**: Reset database with `python manage.py flush` and reapply migrations

## API Documentation

The application provides REST API endpoints through Django REST Framework:

- Authentication endpoints (login, logout, verification)
- Restaurant browsing and filtering
- Order management and tracking
- User profile management

Detailed API documentation available at `/api/` when running the development server.

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a Pull Request

## License

This project is provided for educational and demonstration purposes. Refer to the LICENSE file for complete terms. For commercial use, please contact the project maintainers.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review existing documentation
- Check troubleshooting section above

## Acknowledgments

Built with:
- [Django](https://www.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - REST API toolkit
- [SimpleJWT](https://github.com/jpadilla/django-rest-framework-simplejwt) - JWT authentication
