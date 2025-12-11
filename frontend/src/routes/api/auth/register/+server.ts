import { json } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { JWT_SECRET } from '$lib/server/config';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export async function POST({ request }) {
    const data = await request.json();
    const { first_name, last_name, email, password, phone, role } = data;

    if (!email || !password || !first_name || !last_name || !phone) {
        return json({ detail: 'Missing required fields' }, { status: 400 });
    }

    try {
        // Check if user exists
        const existing = await db.execute({
            sql: 'SELECT id FROM users WHERE email = ?',
            args: [email]
        });

        if (existing.rows.length > 0) {
            return json({ detail: 'Email already registered' }, { status: 400 });
        }

        const hashedPassword = await bcrypt.hash(password, 12);
        const userRole = role || 'driver';

        const result = await db.execute({
            sql: `INSERT INTO users (first_name, last_name, email, hashed_password, phone, role, is_verified, is_active) 
                  VALUES (?, ?, ?, ?, ?, ?, 0, 1) RETURNING id`,
            args: [first_name, last_name, email, hashedPassword, phone, userRole]
        });

        const userId = Number(result.rows[0].id) || Number(result.lastInsertRowid);

        // Generate token immediately
        const token = jwt.sign(
            { sub: email, id: userId, role: userRole },
            JWT_SECRET,
            { expiresIn: '30m' }
        );

        return json({
            access_token: token,
            token_type: 'bearer',
            user: { id: userId, first_name, last_name, email, phone, role: userRole }
        });

    } catch (e: any) {
        console.error(e);
        return json({ detail: 'Registration failed: ' + e.message }, { status: 500 });
    }
}
