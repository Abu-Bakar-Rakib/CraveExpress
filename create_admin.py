import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Check if 'admin' exists, if not create it
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created new admin user. Username: admin, Password: admin123")
else:
    # If it exists, let's just reset the password to be sure
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Updated existing admin user. Username: admin, Password: admin123")
