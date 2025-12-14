"""
Initialize SQLite database with seed data for development
"""
from database import engine, SessionLocal
from models import Base, User
from auth import get_password_hash

def create_seed_data():
    """Create initial seed data for development"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created\n")
    
    db = SessionLocal()
    
    try:
        print("Creating seed data...")
        
        # Create test users
        users = [
            User(
                email="driver@test.com",
                hashed_password=get_password_hash("password123"),
                first_name="John",
                last_name="Driver",
                role="driver",
                phone="+1234567890"
            ),
            User(
                email="provider@test.com",
                hashed_password=get_password_hash("password123"),
                first_name="Mike",
                last_name="Provider",
                role="service_provider",
                phone="+1234567891"
            ),
            User(
                email="admin@test.com",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                role="admin",
                phone="+1234567892"
            )
        ]
        
        print("Creating users...")
        for user in users:
            existing = db.query(User).filter(User.email == user.email).first()
            if not existing:
                db.add(user)
                print(f"  ✓ Created user: {user.email}")
            else:
                print(f"  - User already exists: {user.email}")
        
        db.commit()
        
        print("\n✅ Seed data created successfully!")
        print("\nTest Accounts:")
        print("  Driver:   driver@test.com / password123")
        print("  Provider: provider@test.com / password123")
        print("  Admin:    admin@test.com / admin123")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("VBAMS Database Initialization")
    print("=" * 60)
    print()
    create_seed_data()
    print("\n" + "=" * 60)
