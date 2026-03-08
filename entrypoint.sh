#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
"

exec "$@"