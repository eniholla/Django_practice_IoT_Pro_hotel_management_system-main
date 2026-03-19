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
if [ ! -L assets/Allfiles/css ]; then
  ln -s Css assets/Allfiles/css
fi
if [ ! -L assets/Allfiles/js ]; then
  ln -s Js assets/Allfiles/js
fi
if [ ! -L assets/Allfiles/Css/style.css ]; then
  ln -s Style.css assets/Allfiles/Css/style.css
fi
if [ ! -L assets/Allfiles/Css/responsive.css ]; then
  ln -s Responsive.css assets/Allfiles/Css/responsive.css
fi

python manage.py collectstatic --no-input
python manage.py migrate
