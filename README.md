<div align="center">

# 🍽️ CraveExpress

**A Modern Food Delivery Platform Built with Django**

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.2.x-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-Advanced-red?style=for-the-badge)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)

[Overview](#-overview) • [Features](#-key-features) • [Installation](#-installation--setup) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

CraveExpress is a comprehensive, full-stack food delivery platform that streamlines the entire ordering experience. Built with **Django** and **Django REST Framework**, it provides seamless restaurant browsing, intelligent order management, and real-time delivery tracking—all wrapped in an intuitive, role-based user interface.

**Perfect for restaurants, delivery partners, and customers seeking a modern food delivery solution.**

---

## ✨ Key Features

### 🏪 Restaurant Management
- Browse and search restaurants with advanced filtering
- Detailed restaurant profiles with operating hours and ratings
- Multi-cuisine support and categorization

### 📦 Menu Management
- Comprehensive menu catalog with rich descriptions
- Dynamic pricing and promotional items
- Category-based organization for easy navigation

### 🛒 Shopping Cart & Checkout
- Intuitive cart management with real-time updates
- Multiple payment gateway integration
- Secure checkout process with order confirmation

### 📍 Order & Delivery Tracking
- Real-time order status monitoring
- Live delivery tracking with GPS integration
- Estimated delivery time calculations

### 🔐 Authentication & Authorization
- Secure authentication with phone verification
- **Role-Based Access Control (RBAC)**:
  - 👤 **Customer Dashboard**: Order history, saved addresses, account preferences
  - 🚚 **Delivery Personnel Dashboard**: Active deliveries, route optimization, earnings
  - ⚙️ **Admin Dashboard**: Restaurant management, order analytics, system overview

### 💳 Payment Integration
- Multiple payment gateway support
- Order history and invoice management
- Transaction security and validation

### 📸 Media Management
- Optimized image storage for restaurants and products
- Efficient CDN-ready media handling
- Thumbnail generation for faster loading

---

## 🛠️ System Requirements

| Requirement | Specification |
|---|---|
| **Python** | 3.10 or higher |
| **Database** | SQLite (included) / PostgreSQL (production) |
| **OS** | Windows, macOS, or Linux |
| **Package Manager** | pip (included with Python) |

**Key Dependencies:**
- Django 5.2.x
- Django REST Framework
- SimpleJWT (Token Authentication)
- Pillow (Image Processing)
- NumPy & Shapely (Geospatial Calculations)

---

## 📸 Screenshots

<div align="center">

| Feature | View |
|---------|------|
| **Dashboard** | ![Dashboard](https://github.com/user-attachments/assets/f7efdc9f-7d7f-4098-ae32-2c204360ea33) |
| **Restaurant Browse** | ![Restaurants](https://github.com/user-attachments/assets/5e034c43-d33f-48e1-9bdb-645a8cf6abe2) |
| **Order Management** | ![Orders](https://github.com/user-attachments/assets/284e610d-e76a-4226-a719-3e89fccf3054) |
| **Checkout Process** | ![Checkout](https://github.com/user-attachments/assets/74150cd2-f238-4005-a439-b7250dd82f21) |
| **Delivery Tracking** | ![Tracking](https://github.com/user-attachments/assets/98f4812d-c31a-498c-a1f9-7f6d03fd6d98) |
| **Admin Analytics** | ![Admin](https://github.com/user-attachments/assets/823d1e35-55e4-4639-8e3c-4c6075b476fc) |

</div>

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system
- Git for version control
- Virtual environment support

### Step-by-Step Installation

#### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Abu-Bakar-Rakib/CraveExpress.git
cd CraveExpress
```

#### 2️⃣ **Create and Activate Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

> **⚠️ Windows Users**: If you encounter an execution policy error, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

#### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 4️⃣ **Configure Database**
```bash
# Apply migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser
```

#### 5️⃣ **Load Demo Data (Optional)**
```bash
python manage.py seed_demo
```

#### 6️⃣ **Start Development Server**
```bash
python manage.py runserver
```

#### 7️⃣ **Access the Application**
| Component | URL |
|---|---|
| Application | http://127.0.0.1:8000/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
| API Documentation | http://127.0.0.1:8000/api/ |

---

## 📁 Project Structure

```
CraveExpress/
│
├── 📄 manage.py                    # Django management entry point
├── 📋 requirements.txt             # Python dependencies
├── 🗄️  db.sqlite3                  # Local SQLite database
│
├── 🏗️ cravelexpress/              # Django project configuration
│   ├── settings.py                # Project settings
│   ├── urls.py                    # URL routing
│   ├── wsgi.py                    # WSGI configuration
│   └── asgi.py                    # ASGI configuration
│
├── 🎯 main/                       # Core application
│   ├── models.py                  # Database models & ORM
│   ├── views.py                   # View logic & business rules
│   ├── urls.py                    # App-level URL routing
│   ├── serializers.py             # DRF serializers
│   └── management/
│       └── commands/              # Custom management commands
│
├── 🎨 templates/                  # HTML templates
│   ├── auth/                      # Login & registration
│   ├── restaurant/                # Restaurant listings
│   ├── cart/                      # Shopping cart
│   ├── checkout/                  # Payment & checkout
│   ├── customer/                  # Customer dashboard
│   ├── delivery/                  # Delivery dashboard
│   └── admin/                     # Admin dashboard
│
├── 💾 static/                     # CSS, JavaScript, assets
├── 📦 media/                      # User-uploaded content
└── 🔧 venv/                       # Virtual environment (local)
```

---

## 🔧 Common Commands

### 🗄️ Database Management
```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# View migration status
python manage.py showmigrations

# Reset database (caution!)
python manage.py flush
```

### ✅ Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test main

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage report
coverage run --source='.' manage.py test && coverage report
```

### 📦 Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Clear and recollect static files
python manage.py collectstatic --clear --noinput
```

### 🛠️ Utilities
```bash
# Create new Django app
python manage.py startapp app_name

# Load demo data
python manage.py seed_demo

# Interactive Python shell
python manage.py shell

# Check project configuration
python manage.py check
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Purpose | Default |
|---|---|---|
| `DEBUG` | Development mode flag | `True` |
| `SECRET_KEY` | Django security key | *Configured in settings* |
| `ALLOWED_HOSTS` | Permitted hostnames | `127.0.0.1,localhost` |
| `DATABASE_URL` | Database connection string | SQLite (local) |

### Using a `.env` File

1. Install `python-dotenv`:
   ```bash
   pip install python-dotenv
   ```

2. Create `.env` in project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

3. Load in settings or startup:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### 🚀 Production Deployment

For production environments, ensure:
- ✅ Set `DEBUG = False`
- ✅ Configure a strong `SECRET_KEY`
- ✅ Use PostgreSQL (or production-grade database)
- ✅ Set appropriate `ALLOWED_HOSTS`
- ✅ Collect static files: `python manage.py collectstatic`
- ✅ Use environment variables for sensitive data
- ✅ Enable HTTPS and CSRF protection

---

## 🎬 Media & Assets

- **User Uploads**: Stored in `media/` directory
- **Static Files**: CSS, JavaScript, and static assets in `static/` directory
- **Demo Content**: Load via `python manage.py seed_demo` command
- **Image Optimization**: Automatic thumbnail generation with Pillow

---

## 🐛 Troubleshooting

### 🪟 Windows-Specific Issues

| Issue | Solution |
|---|---|
| Execution Policy Error | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| SQLite Database Locked | Ensure no other processes use `db.sqlite3`, then retry |
| Pillow Installation Issues | Use Python 3.10+ and ensure virtual environment is active |
| Shapely/NumPy Slow Installation | Upgrade pip: `python -m pip install --upgrade pip` |
| Migrations Not Applied | Run `python manage.py makemigrations` then `python manage.py migrate` |

### 🔧 General Troubleshooting

| Issue | Solution |
|---|---|
| Port Already in Use | `python manage.py runserver 8001` |
| Module Not Found | Verify venv activated and dependencies installed |
| Database Migration Errors | `python manage.py flush` and reapply migrations |
| Permission Denied (Linux/macOS) | Use `chmod +x manage.py` for executable permissions |

---

## 📚 API Documentation

CraveExpress provides comprehensive REST API endpoints via Django REST Framework:

### Core Endpoints
- **Authentication**: `/api/auth/` (login, logout, token refresh, phone verification)
- **Restaurants**: `/api/restaurants/` (browse, search, filter, details)
- **Menus**: `/api/menus/` (items, categories, pricing)
- **Orders**: `/api/orders/` (create, track, history, status)
- **Users**: `/api/users/` (profile, addresses, preferences)
- **Deliveries**: `/api/deliveries/` (tracking, assignments, updates)

### Interactive API Docs
- Swagger UI: `/api/swagger/`
- ReDoc: `/api/redoc/`

---

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Submit** a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is provided for **educational and demonstration purposes**. 

For complete terms and conditions, see the [LICENSE](LICENSE) file.

**⚠️ Commercial Use**: Please contact the project maintainers for commercial licensing inquiries.

---

## 💬 Support & Community

Have questions or need help?

- 📝 [Open an Issue](https://github.com/Abu-Bakar-Rakib/CraveExpress/issues)
- 📖 Check the [Troubleshooting](#-troubleshooting) section
- 💡 Review existing documentation
- 🔍 Search closed issues for solutions

---

## 🙏 Acknowledgments

Built with ❤️ using:

| Technology | Purpose |
|---|---|
| [Django](https://www.djangoproject.com/) | Web framework & ORM |
| [Django REST Framework](https://www.django-rest-framework.org/) | REST API development |
| [SimpleJWT](https://github.com/jpadilla/django-rest-framework-simplejwt) | JWT authentication |
| [Pillow](https://python-pillow.org/) | Image processing |
| [Shapely](https://shapely.readthedocs.io/) | Geospatial calculations |

---

<div align="center">

**[⬆ back to top](#-craveexpress)**

Made with 💚 by [Abu Bakar Rakib](https://github.com/Abu-Bakar-Rakib)

</div>
