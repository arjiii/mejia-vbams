import { json } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { JWT_SECRET } from '$lib/server/config';
import jwt from 'jsonwebtoken';

function getUser(request: Request) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
    const token = authHeader.split(' ')[1];
    try {
        return jwt.verify(token, JWT_SECRET) as any;
    } catch {
        return null;
    }
}

export async function GET({ request }) {
    const user = getUser(request);
    if (!user) return json({ detail: 'Not authenticated' }, { status: 401 });

    try {
        const result = await db.execute({
            sql: 'SELECT * FROM vehicles WHERE owner_id = ?',
            args: [user.id]
        });
        return json(result.rows);
    } catch (e) {
        return json({ detail: 'Error fetching vehicles' }, { status: 500 });
    }
}

export async function POST({ request }) {
    const user = getUser(request);
    if (!user) return json({ detail: 'Not authenticated' }, { status: 401 });

    const data = await request.json();

    try {
        const result = await db.execute({
            sql: `INSERT INTO vehicles (owner_id, make, model, year, license_plate, vin, color, vehicle_type, fuel_type, mileage)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *`,
            args: [
                user.id,
                data.make,
                data.model,
                data.year,
                data.license_plate,
                data.vin,
                data.color,
                data.vehicle_type,
                data.fuel_type,
                data.mileage || 0
            ]
        });
        return json(result.rows[0]);
    } catch (e: any) {
        return json({ detail: 'Error creating vehicle: ' + e.message }, { status: 500 });
    }
}
