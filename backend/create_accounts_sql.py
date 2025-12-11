"""
Insert test accounts using raw SQL to bypass any ORM issues
"""
import sqlite3
from auth import get_password_hash

def create_accounts_raw_sql():
    """Create test accounts using raw SQL"""
    
    # Connect to database
    conn = sqlite3.connect('vbams.db')
    cursor = conn.cursor()
    
    try:
        print("Creating test accounts with raw SQL...")
        
        # Test accounts
        accounts = [
            ("driver@test.com", get_password_hash("password123"), "John", "Driver", "driver", "+1234567890"),
            ("provider@test.com", get_password_hash("password123"), "Mike", "Provider", "service_provider", "+1234567891"),
            ("admin@test.com", get_password_hash("admin123"), "Admin", "User", "admin", "+1234567892"),
        ]
        
        for email, password_hash, first_name, last_name, role, phone in accounts:
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing user
                cursor.execute("""
                    UPDATE users 
                    SET hashed_password = ?, first_name = ?, last_name = ?, role = ?, phone = ?, is_verified = 1, is_active = 1
                    WHERE email = ?
                """, (password_hash, first_name, last_name, role, phone, email))
                print(f"✓ Updated: {email}")
            else:
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (email, hashed_password, first_name, last_name, role, phone, is_verified, is_active, latitude, longitude, profile_image)
                    VALUES (?, ?, ?, ?, ?, ?, 1, 1, 0.0, 0.0, '')
                """, (email, password_hash, first_name, last_name, role, phone))
                print(f"✓ Created: {email}")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("Test Accounts Created!")
        print("=" * 60)
        
        # Verify
        print("\nVerifying accounts...")
        cursor.execute("SELECT id, email, role, is_active FROM users")
        users = cursor.fetchall()
        
        for user_id, email, role, is_active in users:
            status = "Active" if is_active else "Inactive"
            print(f"  ID {user_id}: {email} ({role}) - {status}")
        
        print("\n" + "=" * 60)
        print("Login Credentials:")
        print("=" * 60)
        print("DRIVER:           driver@test.com / password123")
        print("SERVICE PROVIDER: provider@test.com / password123")
        print("ADMIN:            admin@test.com / admin123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_accounts_raw_sql()
