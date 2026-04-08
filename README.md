# 🏨 RosegoldHotels

A professional hotel booking management system built with Django, featuring modern security practices, payment integration (Paystack), IoT monitoring, and a responsive frontend.

## Features

- **User Authentication** - Secure registration, login, email verification
- **Role-Based Access** - Admin, Receptionist, and Guest dashboards
- **Booking Management** - Online & offline bookings with conflict detection
- **Room Management** - Categories, pricing, availability tracking
- **Payment Integration** - Paystack payment gateway (Nigerian Naira)
- **Employee Management** - Staff records and salary tracking
- **IoT Alerts** - Real-time room monitoring (temperature, occupancy, etc.)
- **Activity Logging** - Comprehensive audit trail
- **Responsive Design** - Works on desktop and mobile

## Tech Stack

- **Backend**: Django 4.2, Python 3.11+
- **Frontend**: HTML/CSS/JavaScript, Bootstrap, TailwindCSS (dashboard components)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Payments**: Paystack API
- **Deployment**: Render.com ready

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/rosegoldHotels.git
cd rosegoldHotels/RosegoldHotels

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes (production) |
| `DEBUG` | Enable debug mode | No (default: false) |
| `DATABASE_URL` | Database connection string | No (uses SQLite) |
| `PAYSTACK_PUBLIC_KEY` | Paystack public key | For payments |
| `PAYSTACK_SECRET_KEY` | Paystack secret key | For payments |

See `.env.example` for all available options.

## Deployment (Render)

This project includes `render.yaml` for easy Render.com deployment:

1. Connect your GitHub repository to Render
2. Render will automatically detect the `render.yaml` configuration
3. Set required environment variables in the Render dashboard
4. Deploy!

## Project Structure

```
RosegoldHotels/
├── HotelApp/           # Main Django app (views, models, forms)
├── HotelManagementSystem/  # Django project settings
├── alerts/             # IoT monitoring system
├── frontend/           # React/Vite components
├── templates/          # Django templates
├── static/             # Static files source
├── assets/             # Collected static files
├── media/              # User uploads
└── requirements.txt    # Python dependencies
```

## Security

This application implements security best practices:

- HTTPS enforcement in production
- Secure session cookies
- CSRF protection
- HTTP security headers (HSTS, X-Frame-Options, etc.)
- Password validation
- Environment-based configuration

## License

MIT License - see [LICENSE](LICENSE) file.

