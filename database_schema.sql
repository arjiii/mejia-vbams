-- ================================================================
-- VEHICLE BREAKDOWN ASSISTANCE MANAGEMENT SYSTEM (VBAMS)
-- Database Schema - PostgreSQL / MySQL Compatible
-- ================================================================

-- Drop existing tables (in reverse order of dependencies)
DROP TABLE IF EXISTS assistance_requests CASCADE;
DROP TABLE IF EXISTS breakdowns CASCADE;
DROP TABLE IF EXISTS service_providers CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ================================================================
-- USERS TABLE
-- ================================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    role VARCHAR(20) DEFAULT 'driver' CHECK (role IN ('driver', 'service_provider', 'admin')),
    is_verified BOOLEAN DEFAULT FALSE,
    profile_image VARCHAR(255) DEFAULT '',
    latitude DECIMAL(10, 8) DEFAULT 0.0,
    longitude DECIMAL(11, 8) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_created_at (created_at)
);

-- ================================================================
-- VEHICLES TABLE
-- ================================================================
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
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
    last_service_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    next_service_due TIMESTAMP WITH TIME ZONE,
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    insurance_expiry_date TIMESTAMP WITH TIME ZONE,
    iot_device_id VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_vehicles_owner_id (owner_id),
    INDEX idx_vehicles_license_plate (license_plate),
    INDEX idx_vehicles_vin (vin),
    INDEX idx_vehicles_created_at (created_at)
);

-- ================================================================
-- SERVICE PROVIDERS TABLE
-- ================================================================
CREATE TABLE service_providers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    business_name VARCHAR(100) NOT NULL,
    business_license VARCHAR(50) NOT NULL UNIQUE,
    services TEXT,  -- JSON string of service types
    service_radius INTEGER DEFAULT 50,  -- kilometers
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    base_rate DECIMAL(10, 2) NOT NULL,
    per_km_rate DECIMAL(10, 2) DEFAULT 0.0,
    hourly_rate DECIMAL(10, 2) DEFAULT 0.0,
    average_rating DECIMAL(3, 2) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_online BOOLEAN DEFAULT FALSE,
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    last_location_update TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_service_providers_user_id (user_id),
    INDEX idx_service_providers_location (latitude, longitude),
    INDEX idx_service_providers_is_online (is_online),
    INDEX idx_service_providers_created_at (created_at)
);

-- ================================================================
-- BREAKDOWNS TABLE
-- ================================================================
CREATE TABLE breakdowns (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    description TEXT NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('mechanical', 'electrical', 'tire', 'fuel', 'accident', 'other')),
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'reported' CHECK (status IN ('reported', 'assigned', 'in_progress', 'completed', 'cancelled')),
    estimated_cost DECIMAL(10, 2) DEFAULT 0.0,
    actual_cost DECIMAL(10, 2) DEFAULT 0.0,
    service_provider_id INTEGER,
    estimated_arrival_time TIMESTAMP WITH TIME ZONE,
    actual_arrival_time TIMESTAMP WITH TIME ZONE,
    estimated_completion_time TIMESTAMP WITH TIME ZONE,
    actual_completion_time TIMESTAMP WITH TIME ZONE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (service_provider_id) REFERENCES users(id) ON DELETE SET NULL,
    
    -- Indexes
    INDEX idx_breakdowns_vehicle_id (vehicle_id),
    INDEX idx_breakdowns_driver_id (driver_id),
    INDEX idx_breakdowns_status (status),
    INDEX idx_breakdowns_location (latitude, longitude),
    INDEX idx_breakdowns_created_at (created_at)
);

-- ================================================================
-- ASSISTANCE REQUESTS TABLE
-- ================================================================
CREATE TABLE assistance_requests (
    id SERIAL PRIMARY KEY,
    breakdown_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    service_type VARCHAR(20) NOT NULL CHECK (service_type IN ('towing', 'repair', 'fuel_delivery', 'jump_start', 'tire_change', 'lockout', 'diagnostic')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled', 'rejected')),
    assigned_provider_id INTEGER,
    estimated_cost DECIMAL(10, 2) DEFAULT 0.0,
    actual_cost DECIMAL(10, 2) DEFAULT 0.0,
    estimated_arrival_time TIMESTAMP WITH TIME ZONE,
    actual_arrival_time TIMESTAMP WITH TIME ZONE,
    estimated_completion_time TIMESTAMP WITH TIME ZONE,
    actual_completion_time TIMESTAMP WITH TIME ZONE,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (breakdown_id) REFERENCES breakdowns(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_provider_id) REFERENCES users(id) ON DELETE SET NULL,
    
    -- Indexes
    INDEX idx_assistance_requests_breakdown_id (breakdown_id),
    INDEX idx_assistance_requests_requester_id (requester_id),
    INDEX idx_assistance_requests_status (status),
    INDEX idx_assistance_requests_location (latitude, longitude),
    INDEX idx_assistance_requests_created_at (created_at)
);

-- ================================================================
-- SAMPLE DATA INSERT
-- ================================================================

-- Insert sample users
INSERT INTO users (first_name, last_name, email, hashed_password, phone, role, is_verified, is_active) VALUES
('John', 'Doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567890', 'driver', TRUE, TRUE),
('Jane', 'Smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567891', 'service_provider', TRUE, TRUE),
('Admin', 'User', 'admin@vbams.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567892', 'admin', TRUE, TRUE),
('Mike', 'Johnson', 'mike.j@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567893', 'driver', TRUE, TRUE),
('Sarah', 'Williams', 'sarah.w@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqq3V9/XG.', '+1234567894', 'service_provider', TRUE, TRUE);

-- Insert sample vehicles
INSERT INTO vehicles (owner_id, make, model, year, license_plate, vin, color, vehicle_type, fuel_type, mileage) VALUES
(1, 'Toyota', 'Camry', 2020, 'ABC123', '1HGBH41JXMN109186', 'Silver', 'car', 'gasoline', 45000),
(1, 'Honda', 'Civic', 2019, 'XYZ789', '2HGBH41JXMN109187', 'Blue', 'car', 'gasoline', 32000),
(4, 'Ford', 'F-150', 2021, 'TRK456', '3HGBH41JXMN109188', 'Black', 'truck', 'diesel', 28000),
(4, 'Tesla', 'Model 3', 2022, 'EV2022', '4HGBH41JXMN109189', 'White', 'car', 'electric', 15000);

-- Insert sample service providers
INSERT INTO service_providers (user_id, business_name, business_license, services, service_radius, latitude, longitude, base_rate, per_km_rate, hourly_rate, is_verified, is_online) VALUES
(2, 'Quick Fix Auto Services', 'BL-2024-001', '["towing", "repair", "jump_start", "tire_change"]', 50, 14.5995, 120.9842, 50.00, 2.50, 75.00, TRUE, TRUE),
(5, 'Road Rescue Inc.', 'BL-2024-002', '["towing", "fuel_delivery", "lockout", "diagnostic"]', 75, 14.6091, 121.0223, 75.00, 3.00, 100.00, TRUE, FALSE);

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

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_providers_updated_at BEFORE UPDATE ON service_providers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_breakdowns_updated_at BEFORE UPDATE ON breakdowns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assistance_requests_updated_at BEFORE UPDATE ON assistance_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ================================================================
-- VIEWS FOR COMMON QUERIES
-- ================================================================

-- View for active breakdowns with vehicle and driver info
CREATE OR REPLACE VIEW active_breakdowns_view AS
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
CREATE OR REPLACE VIEW available_service_providers_view AS
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
WHERE sp.is_active = TRUE AND sp.is_verified = TRUE;

-- View for assistance request details
CREATE OR REPLACE VIEW assistance_request_details_view AS
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
-- INDEXES FOR GEOSPATIAL QUERIES (if using PostGIS)
-- ================================================================
-- Uncomment these if you're using PostGIS extension
-- CREATE INDEX idx_breakdowns_location_gist ON breakdowns USING GIST(point(longitude, latitude));
-- CREATE INDEX idx_service_providers_location_gist ON service_providers USING GIST(point(longitude, latitude));
-- CREATE INDEX idx_assistance_requests_location_gist ON assistance_requests USING GIST(point(longitude, latitude));

-- ================================================================
-- GRANT PERMISSIONS (adjust as needed for your environment)
-- ================================================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vbams_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vbams_user;

-- ================================================================
-- END OF SCHEMA
-- ================================================================
