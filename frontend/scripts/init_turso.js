import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SQL_FILE_PATH = path.join(__dirname, '../../database_schema_sqlite.sql');

// Configuration (duplicated here for script usage)
const TURSO_DB_URL = 'libsql://vbams-piksel.aws-ap-northeast-1.turso.io';
const TURSO_DB_TOKEN = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NjU0Mzg3ODYsImlkIjoiNTU2MjRjOTctODU2Mi00MzBhLWI0NWUtZjUxNGZlMDFiNmIxIiwicmlkIjoiYjA5OGUxM2QtZjc4ZC00MzlkLWIzZWItYjUwZDM0NGIzZjIzIn0.lUZjI2_oG9Q_sQwVmCn45JsO1Mwxiif-xDLCWbc3tWPC9kVSUHqlmd4pTGVZPFZozJRpqLkpKtRRhjq880t9Cw';

const db = createClient({
    url: TURSO_DB_URL,
    authToken: TURSO_DB_TOKEN,
});

async function main() {
    console.log('Reading SQL schema...');
    try {
        const sqlContent = fs.readFileSync(SQL_FILE_PATH, 'utf-8');

        // Split by semicolon but ignore newlines to get individual statements
        // This is a naive split, but sufficient for the provided schema
        const statements = sqlContent
            .split(';')
            .map(s => s.trim())
            .filter(s => s.length > 0);

        console.log(`Found ${statements.length} statements.`);

        for (const stmt of statements) {
            // Skip comments and empty lines
            if (stmt.startsWith('--') || !stmt) continue;

            try {
                console.log(`Executing: ${stmt.substring(0, 50)}...`);
                await db.execute(stmt);
            } catch (err) {
                console.error('Error executing statement:', err.message);
                // Don't stop on error (e.g. drop table if exists might fail if not exists in some restricted modes, but usually fine)
            }
        }

        console.log('Database initialization completed.');
    } catch (err) {
        console.error('Failed to read or execute SQL:', err);
    }
}

main();
