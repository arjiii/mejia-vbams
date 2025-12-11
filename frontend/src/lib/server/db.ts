import { createClient } from '@libsql/client';
import { TURSO_DB_URL, TURSO_DB_TOKEN } from './config';

export const db = createClient({
    url: TURSO_DB_URL,
    authToken: TURSO_DB_TOKEN,
});

export type User = {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    hashed_password: string;
    phone: string;
    role: 'driver' | 'service_provider' | 'admin';
    is_verified: number; // 0 or 1
    profile_image: string;
    latitude: number;
    longitude: number;
    is_active: number; // 0 or 1
    created_at: string;
    updated_at: string;
};

export type Vehicle = {
    id: number;
    owner_id: number;
    make: string;
    model: string;
    year: number;
    license_plate: string;
    vin: string;
    color: string;
    vehicle_type: string;
    fuel_type: string;
    mileage: number;
    last_service_date: string;
    is_active: number;
};

export type Breakdown = {
    id: number;
    vehicle_id: number;
    driver_id: number;
    latitude: number;
    longitude: number;
    address: string;
    description: string;
    category: string;
    severity: string;
    status: string;
    created_at: string;
};
