#!/usr/bin/env bash
# Render build script for Hotel Management System
set -o errexit

# Ensure we run from the script's own directory
cd "$(dirname "$0")"

pip install --upgrade pip
pip install -r requirements.txt

# Build the React frontend
cd frontend
npm ci
npm run build
cd ..

# Ensure lowercase symlinks exist so Django templates can reference
# Allfiles/css/... and Allfiles/js/... (assets/ uses capital Css/Js/)
mkdir -p "assets/Allfiles/Css" "assets/Allfiles/Js"
ln -sfn "Css" "assets/Allfiles/css"
ln -sfn "Js" "assets/Allfiles/js"

python manage.py collectstatic --no-input

python manage.py migrate

# Optionally create a default superuser if requested via environment variables.
# To enable, set CREATE_DEFAULT_SUPERUSER=1 and provide SUPERUSER_EMAIL and
# SUPERUSER_PASSWORD in the environment before running this script.
if [ "${CREATE_DEFAULT_SUPERUSER:-}" = "1" ]; then
  python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()

email = os.environ.get('SUPERUSER_EMAIL')
password = os.environ.get('SUPERUSER_PASSWORD')

if not email or not password:
    raise SystemExit('SUPERUSER_EMAIL and SUPERUSER_PASSWORD must be set when CREATE_DEFAULT_SUPERUSER=1')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
"
fi
