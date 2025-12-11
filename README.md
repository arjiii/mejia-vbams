# Vehicle Breakdown Assistance Management System (VBAMS)

A comprehensive system for managing vehicle breakdowns with real-time assistance, GPS tracking, and AI-powered predictive maintenance.

## Project Overview

The Vehicle Breakdown Assistance Management System (VBAMS) addresses the critical need for efficient, technology-driven roadside assistance. This system integrates multiple emerging technologies to provide a seamless experience for drivers, service providers, and fleet managers.

## Key Features Implemented

### ✅ Completed Features

1. **Backend API (FastAPI)**
   - User authentication and authorization with JWT
   - Vehicle registration and management
   - Breakdown reporting system
   - Service provider management
   - Real-time assistance requests
   - WebSocket communication for real-time updates

2. **Database Design**
   - PostgreSQL with SQLAlchemy ORM
   - Comprehensive data models for users, vehicles, breakdowns, and assistance requests
   - Geospatial indexing for location-based queries

3. **Frontend Interface**
   - Responsive web interface with Bootstrap
   - User dashboard with real-time statistics
   - Vehicle management system
   - Breakdown reporting interface
   - Profile management

4. **Real-time Communication**
   - WebSocket implementation for instant messaging
   - Location tracking and updates
   - Status notifications

### 🚧 Pending Features

1. **GPS-based Location Tracking**
   - Google Maps API integration
   - Real-time location updates
   - Geofencing capabilities

2. **AI-Powered Predictive Features**
   - Machine learning models for failure prediction
   - Preventive maintenance suggestions
   - Pattern recognition in breakdown data

3. **IoT Integration**
   - Vehicle monitoring devices
   - Real-time diagnostics
   - Sensor data integration

4. **Cloud Deployment**
   - AWS S3 for file storage
   - Redis for caching
   - Docker containerization

## Technology Stack

- **Backend**: Python FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: JWT tokens with bcrypt
- **Real-time**: WebSocket connections
- **Maps**: Google Maps API (pending)
- **AI/ML**: TensorFlow, scikit-learn (pending)
- **Cloud**: AWS services (pending)

## Project Structure

```
mejia/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # Authentication utilities
│   ├── websocket_manager.py   # WebSocket management
│   ├── routers/               # API routes
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── vehicles.py
│   │   ├── breakdowns.py
│   │   ├── service_providers.py
│   │   └── assistance.py
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
└── frontend/
    ├── index.html            # Landing page
    └── dashboard.html        # User dashboard
```

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for frontend development)

### Backend Setup

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up database**
   ```bash
   createdb vbams
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Open the HTML files**
   - `frontend/index.html` - Landing page
   - `frontend/dashboard.html` - User dashboard

2. **Configure API endpoint**
   - Update `API_BASE_URL` in JavaScript files to match your backend URL

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Vehicles
- `POST /api/vehicles` - Register vehicle
- `GET /api/vehicles` - Get user vehicles
- `PUT /api/vehicles/{id}` - Update vehicle
- `DELETE /api/vehicles/{id}` - Delete vehicle

### Breakdowns
- `POST /api/breakdowns` - Report breakdown
- `GET /api/breakdowns` - Get breakdowns
- `PUT /api/breakdowns/{id}` - Update breakdown

### Service Providers
- `POST /api/service-providers/register` - Register as provider
- `GET /api/service-providers/profile` - Get provider profile
- `PUT /api/service-providers/location` - Update location

### Assistance
- `POST /api/assistance` - Create assistance request
- `GET /api/assistance` - Get assistance requests
- `PUT /api/assistance/{id}/accept` - Accept request

## WebSocket Endpoints

- `WS /ws/{client_id}` - Real-time communication

## Key Features Explained

### 1. User Management
- Role-based access control (Driver, Service Provider, Admin)
- JWT-based authentication
- Profile management with location tracking

### 2. Vehicle Management
- Comprehensive vehicle registration
- Maintenance tracking
- IoT device integration support

### 3. Breakdown Reporting
- Real-time breakdown reporting
- GPS location integration
- Categorization and severity levels
- Image upload support

### 4. Service Provider System
- Provider registration and verification
- Service area management
- Real-time availability status
- Rating and review system

### 5. Assistance Request System
- Automated provider matching
- Real-time status updates
- Cost estimation and tracking
- Payment integration support

## Future Enhancements

1. **AI Integration**
   - Predictive maintenance algorithms
   - Failure pattern recognition
   - Automated service recommendations

2. **IoT Integration**
   - Real-time vehicle diagnostics
   - Sensor data collection
   - Automated breakdown detection

3. **Mobile Applications**
   - Native iOS and Android apps
   - Push notifications
   - Offline capability

4. **Advanced Analytics**
   - Dashboard analytics
   - Performance metrics
   - Business intelligence reports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the development team.
