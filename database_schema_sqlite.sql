-- ================================================================
-- VEHICLE BREAKDOWN ASSISTANCE MANAGEMENT SYSTEM (VBAMS)
-- Database Schema - SQLite Compatible
-- ================================================================

-- Drop existing tables (in reverse order of dependencies)
DROP TABLE IF EXISTS assistance_requests;
DROP TABLE IF EXISTS breakdowns;
DROP TABLE IF EXISTS service_providers;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS users;

-- ================================================================
-- USERS TABLE
-- ================================================================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    role VARCHAR(20) DEFAULT 'driver' CHECK (role IN ('driver', 'service_provider', 'admin')),
    is_verified BOOLEAN DEFAULT 0,
    profile_image VARCHAR(255) DEFAULT '',
    latitude REAL DEFAULT 0.0,
    longitude REAL DEFAULT 0.0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ================================================================
-- VEHICLES TABLE
-- ================================================================
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    license_plate VARCHAR(20) NOT NULL UNIQUE,
    vin VARCHAR(17) NOT NULL UNIQUE,
    color VARCHAR(30) NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('car', 'truck', 'motorcycle', 'bus', 'van')),
    fuel_type VARCHAR(20) NOT NULL CHECK (fuel_type IN ('gasoline', 'diesel', 'electric', 'hybrid', 'lpg')),
    mileage INTEGER DEFAULT 0,
    last_service_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    next_service_due DATETIME,
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    insurance_expiry_date DATETIME,
    iot_device_id VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_vehicles_owner_id ON vehicles(owner_id);
CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX idx_vehicles_vin ON vehicles(vin);
CREATE INDEX idx_vehicles_created_at ON vehicles(created_at);

-- ================================================================
-- SERVICE PROVIDERS TABLE
-- ================================================================
CREATE TABLE service_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    business_name VARCHAR(100) NOT NULL,
    business_license VARCHAR(50) NOT NULL UNIQUE,
    services TEXT,
    service_radius INTEGER DEFAULT 50,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    base_rate REAL NOT NULL,
    per_km_rate REAL DEFAULT 0.0,
    hourly_rate REAL DEFAULT 0.0,
    average_rating REAL DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    is_online BOOLEAN DEFAULT 0,
    current_latitude REAL,
    current_longitude REAL,
    last_location_update DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_service_providers_user_id ON service_providers(user_id);
CREATE INDEX idx_service_providers_latitude ON service_providers(latitude);
CREATE INDEX idx_service_providers_longitude ON service_providers(longitude);
CREATE INDEX idx_service_providers_is_online ON service_providers(is_online);
CREATE INDEX idx_service_providers_created_at ON service_providers(created_at);

-- ================================================================
-- BREAKDOWNS TABLE
-- ================================================================
CREATE TABLE breakdowns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    description TEXT NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('mechanical', 'electrical', 'tire', 'fuel', 'accident', 'other')),
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'reported' CHECK (status IN ('reported', 'assigned', 'in_progress', 'completed', 'cancelled')),
    estimated_cost REAL DEFAULT 0.0,
    actual_cost REAL DEFAULT 0.0,
    service_provider_id INTEGER,
    estimated_arrival_time DATETIME,
    actual_arrival_time DATETIME,
    estimated_completion_time DATETIME,
    actual_completion_time DATETIME,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    is_resolved BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (service_provider_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_breakdowns_vehicle_id ON breakdowns(vehicle_id);
CREATE INDEX idx_breakdowns_driver_id ON breakdowns(driver_id);
CREATE INDEX idx_breakdowns_status ON breakdowns(status);
CREATE INDEX idx_breakdowns_latitude ON breakdowns(latitude);
CREATE INDEX idx_breakdowns_longitude ON breakdowns(longitude);
CREATE INDEX idx_breakdowns_created_at ON breakdowns(created_at);

-- ================================================================
-- ASSISTANCE REQUESTS TABLE
-- ================================================================
CREATE TABLE assistance_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breakdown_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    service_type VARCHAR(20) NOT NULL CHECK (service_type IN ('towing', 'repair', 'fuel_delivery', 'jump_start', 'tire_change', 'lockout', 'diagnostic')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled', 'rejected')),
    assigned_provider_id INTEGER,
    estimated_cost REAL DEFAULT 0.0,
    actual_cost REAL DEFAULT 0.0,
    estimated_arrival_time DATETIME,
    actual_arrival_time DATETIME,
    estimated_completion_time DATETIME,
    actual_completion_time DATETIME,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    address VARCHAR(255),
    special_instructions TEXT,
    contact_phone VARCHAR(20),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    payment_method VARCHAR(20) CHECK (payment_method IN ('cash', 'credit_card', 'debit_card', 'mobile_payment')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (breakdown_id) REFERENCES breakdowns(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_provider_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_assistance_requests_breakdown_id ON assistance_requests(breakdown_id);
CREATE INDEX idx_assistance_requests_requester_id ON assistance_requests(requester_id);
CREATE INDEX idx_assistance_requests_status ON assistance_requests(status);
CREATE INDEX idx_assistance_requests_latitude ON assistance_requests(latitude);
CREATE INDEX idx_assistance_requests_longitude ON assistance_requests(longitude);
CREATE INDEX idx_assistance_requests_created_at ON assistance_requests(created_at);

-- ================================================================
-- SAMPLE DATA INSERT
-- ================================================================

-- Insert sample users (password is 'password123' hashed with bcrypt)
INSERT INTO users (first_name, last_name, email, hashed_password, phone, role, is_verified, is_active) VALUES
('John', 'Doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567890', 'driver', 1, 1),
('Jane', 'Smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567891', 'service_provider', 1, 1),
('Admin', 'User', 'admin@vbams.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567892', 'admin', 1, 1),
('Mike', 'Johnson', 'mike.j@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567893', 'driver', 1, 1),
('Sarah', 'Williams', 'sarah.w@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567894', 'service_provider', 1, 1);

-- Insert sample vehicles
INSERT INTO vehicles (owner_id, make, model, year, license_plate, vin, color, vehicle_type, fuel_type, mileage) VALUES
(1, 'Toyota', 'Camry', 2020, 'ABC123', '1HGBH41JXMN109186', 'Silver', 'car', 'gasoline', 45000),
(1, 'Honda', 'Civic', 2019, 'XYZ789', '2HGBH41JXMN109187', 'Blue', 'car', 'gasoline', 32000),
(4, 'Ford', 'F-150', 2021, 'TRK456', '3HGBH41JXMN109188', 'Black', 'truck', 'diesel', 28000),
(4, 'Tesla', 'Model 3', 2022, 'EV2022', '4HGBH41JXMN109189', 'White', 'car', 'electric', 15000);

-- Insert sample service providers
INSERT INTO service_providers (user_id, business_name, business_license, services, service_radius, latitude, longitude, base_rate, per_km_rate, hourly_rate, is_verified, is_online) VALUES
(2, 'Quick Fix Auto Services', 'BL-2024-001', '["towing", "repair", "jump_start", "tire_change"]', 50, 14.5995, 120.9842, 50.00, 2.50, 75.00, 1, 1),
(5, 'Road Rescue Inc.', 'BL-2024-002', '["towing", "fuel_delivery", "lockout", "diagnostic"]', 75, 14.6091, 121.0223, 75.00, 3.00, 100.00, 1, 0);

-- Insert sample breakdowns
INSERT INTO breakdowns (vehicle_id, driver_id, latitude, longitude, address, city, state, country, description, category, severity, status) VALUES
(1, 1, 14.5995, 120.9842, '123 Main Street', 'Manila', 'Metro Manila', 'Philippines', 'Engine overheating, smoke coming from hood', 'mechanical', 'high', 'reported'),
(3, 4, 14.6091, 121.0223, '456 Highway Road', 'Quezon City', 'Metro Manila', 'Philippines', 'Flat tire on highway', 'tire', 'medium', 'assigned');

-- Insert sample assistance requests
INSERT INTO assistance_requests (breakdown_id, requester_id, service_type, priority, latitude, longitude, address, contact_phone, status) VALUES
(1, 1, 'towing', 'high', 14.5995, 120.9842, '123 Main Street', '+1234567890', 'pending'),
(2, 4, 'tire_change', 'medium', 14.6091, 121.0223, '456 Highway Road', '+1234567893', 'accepted');

-- ================================================================
-- TRIGGERS FOR UPDATED_AT TIMESTAMP
-- ================================================================

-- Trigger for users table
CREATE TRIGGER update_users_updated_at 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger for vehicles table
CREATE TRIGGER update_vehicles_updated_at 
AFTER UPDATE ON vehicles
FOR EACH ROW
BEGIN
    UPDATE vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger for service_providers table
CREATE TRIGGER update_service_providers_updated_at 
AFTER UPDATE ON service_providers
FOR EACH ROW
BEGIN
    UPDATE service_providers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger for breakdowns table
CREATE TRIGGER update_breakdowns_updated_at 
AFTER UPDATE ON breakdowns
FOR EACH ROW
BEGIN
    UPDATE breakdowns SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger for assistance_requests table
CREATE TRIGGER update_assistance_requests_updated_at 
AFTER UPDATE ON assistance_requests
FOR EACH ROW
BEGIN
    UPDATE assistance_requests SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ================================================================
-- VIEWS FOR COMMON QUERIES
-- ================================================================

-- View for active breakdowns with vehicle and driver info
CREATE VIEW active_breakdowns_view AS
SELECT 
    b.id,
    b.description,
    b.category,
    b.severity,
    b.status,
    b.latitude,
    b.longitude,
    b.address,
    b.created_at,
    v.make,
    v.model,
    v.license_plate,
    u.first_name,
    u.last_name,
    u.phone
FROM breakdowns b
JOIN vehicles v ON b.vehicle_id = v.id
JOIN users u ON b.driver_id = u.id
WHERE b.status IN ('reported', 'assigned', 'in_progress');

-- View for available service providers
CREATE VIEW available_service_providers_view AS
SELECT 
    sp.id,
    sp.business_name,
    sp.services,
    sp.service_radius,
    sp.latitude,
    sp.longitude,
    sp.base_rate,
    sp.average_rating,
    sp.is_online,
    u.first_name,
    u.last_name,
    u.phone,
    u.email
FROM service_providers sp
JOIN users u ON sp.user_id = u.id
WHERE sp.is_active = 1 AND sp.is_verified = 1;

-- View for assistance request details
CREATE VIEW assistance_request_details_view AS
SELECT 
    ar.id,
    ar.service_type,
    ar.priority,
    ar.status,
    ar.latitude,
    ar.longitude,
    ar.address,
    ar.created_at,
    b.description AS breakdown_description,
    b.category AS breakdown_category,
    u.first_name AS requester_first_name,
    u.last_name AS requester_last_name,
    u.phone AS requester_phone
FROM assistance_requests ar
JOIN breakdowns b ON ar.breakdown_id = b.id
JOIN users u ON ar.requester_id = u.id;

-- ================================================================
-- END OF SCHEMA
-- ================================================================
