import { json } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { JWT_SECRET } from '$lib/server/config';
import jwt from 'jsonwebtoken';

export async function GET({ request }) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return json({ detail: 'Not authenticated' }, { status: 401 });
    }

    const token = authHeader.split(' ')[1];

    try {
        const payload = jwt.verify(token, JWT_SECRET) as any;

        const result = await db.execute({
            sql: 'SELECT id, first_name, last_name, email, phone, role, is_verified, profile_image, latitude, longitude, is_active FROM users WHERE id = ?',
            args: [payload.id]
        });

        if (result.rows.length === 0) {
            return json({ detail: 'User not found' }, { status: 404 });
        }

        const user = result.rows[0];
        return json(user);

    } catch (e) {
        return json({ detail: 'Invalid token' }, { status: 401 });
    }
}
