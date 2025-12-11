# Vehicle Breakdown Assistance Management System (VBAMS)

A comprehensive FastAPI-based system for managing vehicle breakdowns with real-time assistance, GPS tracking, and AI-powered predictive maintenance.

## Features

- **User Management**: Registration, authentication, and role-based access control
- **Vehicle Management**: Vehicle registration, tracking, and maintenance records
- **Breakdown Reporting**: Real-time breakdown reporting with GPS location
- **Service Provider Management**: Service provider registration and management
- **Real-time Communication**: WebSocket-based communication between drivers and service providers
- **GPS Tracking**: Location-based services and tracking
- **AI Integration**: Predictive maintenance and failure prediction
- **IoT Integration**: Vehicle monitoring and diagnostics
- **Cloud Deployment**: Scalable cloud-based architecture

## Technology Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Real-time Communication**: WebSocket
- **AI/ML**: TensorFlow, scikit-learn
- **IoT**: REST API integration
- **Cloud**: AWS S3, Redis
- **Maps**: Google Maps API
- **Testing**: pytest

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication utilities
├── websocket_manager.py   # WebSocket connection manager
├── routers/               # API route handlers
│   ├── auth.py           # Authentication routes
│   ├── users.py          # User management routes
│   ├── vehicles.py       # Vehicle management routes
│   ├── breakdowns.py      # Breakdown reporting routes
│   ├── service_providers.py # Service provider routes
│   └── assistance.py     # Assistance request routes
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mejia/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Install PostgreSQL and create database
   createdb vbams
   
   # Run migrations (when Alembic is set up)
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/update-location` - Update user location

### Vehicles
- `POST /api/vehicles` - Register new vehicle
- `GET /api/vehicles` - Get user's vehicles
- `GET /api/vehicles/{id}` - Get specific vehicle
- `PUT /api/vehicles/{id}` - Update vehicle
- `DELETE /api/vehicles/{id}` - Delete vehicle

### Breakdowns
- `POST /api/breakdowns` - Report breakdown
- `GET /api/breakdowns` - Get user's breakdowns
- `GET /api/breakdowns/{id}` - Get specific breakdown
- `PUT /api/breakdowns/{id}` - Update breakdown

### Service Providers
- `POST /api/service-providers/register` - Register as service provider
- `GET /api/service-providers/profile` - Get provider profile
- `PUT /api/service-providers/profile` - Update profile
- `PUT /api/service-providers/location` - Update location

### Assistance
- `POST /api/assistance` - Create assistance request
- `GET /api/assistance` - Get assistance requests
- `PUT /api/assistance/{id}/accept` - Accept request
- `PUT /api/assistance/{id}/complete` - Complete request

## WebSocket Endpoints

- `WS /ws/{client_id}` - WebSocket connection for real-time communication

## Environment Variables

Key environment variables to configure:

- `DATABASE_URL` - Full SQLAlchemy database URL (for example, a MySQL URL using PyMySQL: `mysql+pymysql://user:pass@host:3306/dbname`). If not set, the app builds a URL from the `DB_*` variables below.
- `SECRET_KEY` - JWT secret key
- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `REDIS_URL` - Redis connection string

If you prefer to run the database locally using XAMPP (MySQL / MariaDB), you can use the `DB_*` variables instead of a full `DATABASE_URL`.

Using XAMPP (MySQL)

1. Start XAMPP and ensure MySQL is running.
2. Create a database named `vbams` (or choose another name and set `DB_NAME` accordingly).
3. Copy `backend/.env.example` to `backend/.env` and update the following values:

```
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=vbams
```

4. Run the app normally (the database URL will be constructed automatically from these `DB_*` values when `DATABASE_URL` is not present).

Note: `pymysql` is included in `requirements.txt` so SQLAlchemy can connect to a MySQL (XAMPP) instance.

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
mypy .
```

## Deployment

The application is designed for cloud deployment with:
- PostgreSQL database
- Redis for caching
- AWS S3 for file storage
- Docker containerization support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
