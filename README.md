# TestProject (Django)

A Django-based web app with restaurant browsing, menu items, cart/checkout, delivery, and basic payment integration. Includes admin dashboards for staff, customer and delivery views, and demo seed data for easy local testing.

## Features
- Restaurant listing and details (`templates/restaurant/`)
- Menu items, cart, and checkout (`templates/cart/`, `templates/checkout/`)
- Customer, delivery, and admin dashboards (`templates/customer/`, `templates/delivery/`, `templates/admin/`)
- Authentication with login and phone verification (`templates/auth/`)
- Image uploads to `media/`
- Admin site at `/admin/`

## Requirements
- Python 3.10+ (Windows supported)
- pip (comes with Python)
- SQLite (bundled, no setup needed)

Python dependencies are pinned in `requirements.txt` (Django 5.2.x, DRF, SimpleJWT, Pillow, NumPy, Shapely, etc.).

## Quick Start (Windows PowerShell)
```powershell
# From project root
cd E:\Code\Python\TestProject

# 1) Create & activate virtualenv (skip if venv/ already exists)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Database migrations
python manage.py migrate

# 4) Create an admin user
python manage.py createsuperuser

# 5) (Optional) Load demo data
python manage.py seed_demo

# 6) Run the server
python manage.py runserver
```
Now open `http://127.0.0.1:8000/` in your browser. The admin is at `http://127.0.0.1:8000/admin/`.

## Project Structure (high level)
```
TestProject/
  manage.py
  requirements.txt
  testproject/            # Django project settings
  main/                   # Main app: models, views, urls, mgmt commands
  templates/              # HTML templates (home, auth, restaurant, cart, etc.)
  static/                 # CSS/JS/images (served in development)
  media/                  # Uploaded images (e.g. restaurant images)
  db.sqlite3              # SQLite database (local dev)
  venv/                   # Virtual environment (local-only)
```

## Common Commands
```powershell
# Run tests
python manage.py test

# Create a new app (example)
python manage.py startapp myapp

# Make and apply model changes
python manage.py makemigrations
python manage.py migrate

# Collect static files for production (optional)
python manage.py collectstatic
```

## Configuration
The default settings module is `testproject.settings`.

Environment variables you may want to set (optional):
- `DEBUG` (default True in development): `True` or `False`
- `SECRET_KEY`: set a strong secret for production
- `ALLOWED_HOSTS`: e.g. `127.0.0.1,localhost`

If you use a `.env` file, ensure it is loaded (e.g., via `python-dotenv` or your own loader). This project works out-of-the-box with SQLite and the provided settings for local dev.

## Data & Media
- User-uploaded images are stored under `media/`.
- Example placeholder assets live under `static/`.
- Demo content can be created with: `python manage.py seed_demo`.

## Troubleshooting (Windows)
- Virtualenv activation policy error:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```
- SQLite locked error: stop other processes using `db.sqlite3`, then retry.
- Pillow install issues: ensure you have a recent Python version (3.10+) and use the virtualenv. Wheels in `requirements.txt` should install automatically.
- Shapely/NumPy slow install: prebuilt wheels are used; if it compiles, upgrade pip: `python -m pip install --upgrade pip` and retry.
- Migrations not picked up: run `python manage.py makemigrations` then `python manage.py migrate`.

## Useful URLs
- Home: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## License
This project is for learning/demo purposes. Add a LICENSE file if you plan to distribute.
