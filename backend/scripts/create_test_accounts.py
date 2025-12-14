"""
Directly insert test accounts into the database
"""
from database import SessionLocal
from models import User
from auth import get_password_hash

def create_test_accounts():
    """Create test accounts for each role"""
    db = SessionLocal()
    
    try:
        print("Creating test accounts...")
        
        # Test accounts data
        accounts = [
            {
                "email": "driver@test.com",
                "hashed_password": get_password_hash("password123"),
                "first_name": "John",
                "last_name": "Driver",
                "role": "driver",
                "phone": "+1234567890",
                "is_verified": True,
                "is_active": True
            },
            {
                "email": "provider@test.com",
                "hashed_password": get_password_hash("password123"),
                "first_name": "Mike",
                "last_name": "Provider",
                "role": "service_provider",
                "phone": "+1234567891",
                "is_verified": True,
                "is_active": True
            },
            {
                "email": "admin@test.com",
                "hashed_password": get_password_hash("admin123"),
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "phone": "+1234567892",
                "is_verified": True,
                "is_active": True
            }
        ]
        
        for account_data in accounts:
            # Check if user already exists
            existing = db.query(User).filter(User.email == account_data["email"]).first()
            
            if existing:
                print(f"✓ User already exists: {account_data['email']}")
                # Update password in case it was wrong
                existing.hashed_password = account_data["hashed_password"]
                db.commit()
                print(f"  → Password updated for {account_data['email']}")
            else:
                # Create new user
                new_user = User(**account_data)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                print(f"✓ Created user: {account_data['email']} (ID: {new_user.id})")
        
        print("\n" + "=" * 60)
        print("Test Accounts Created Successfully!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print("-" * 60)
        print("DRIVER:")
        print("  Email:    driver@test.com")
        print("  Password: password123")
        print("\nSERVICE PROVIDER:")
        print("  Email:    provider@test.com")
        print("  Password: password123")
        print("\nADMIN:")
        print("  Email:    admin@test.com")
        print("  Password: admin123")
        print("=" * 60)
        
        # Verify they were created
        print("\nVerifying accounts...")
        for account_data in accounts:
            user = db.query(User).filter(User.email == account_data["email"]).first()
            if user:
                print(f"✓ {account_data['email']} - ID: {user.id}, Role: {user.role}")
            else:
                print(f"✗ {account_data['email']} - NOT FOUND!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_accounts()
