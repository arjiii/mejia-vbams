import { json } from '@sveltejs/kit';
import { db, type User } from '$lib/server/db';
import { JWT_SECRET } from '$lib/server/config';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export async function POST({ request }) {
    const { email, password } = await request.json();

    if (!email || !password) {
        return json({ detail: 'Email and password are required' }, { status: 400 });
    }

    try {
        const result = await db.execute({
            sql: 'SELECT * FROM users WHERE email = ?',
            args: [email]
        });

        if (result.rows.length === 0) {
            return json({ detail: 'Invalid credentials' }, { status: 401 });
        }

        const user = result.rows[0] as unknown as User;

        // Check password
        const isValid = await bcrypt.compare(password, user.hashed_password);

        if (!isValid) {
            return json({ detail: 'Invalid credentials' }, { status: 401 });
        }

        // Generate Token
        const token = jwt.sign(
            { sub: user.email, id: user.id, role: user.role },
            JWT_SECRET,
            { expiresIn: '30m' }
        );

        return json({ access_token: token, token_type: 'bearer' });

    } catch (e: any) {
        console.error(e);
        return json({ detail: 'Internal server error' }, { status: 500 });
    }
}
