"""
Script to create an admin user in the database
Run this once to create the initial admin account
"""
import sys
import os

# Add parent directory to path to import from backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import User
from auth import get_password_hash

def create_admin():
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Admin credentials
        admin_email = "admin@vbams.com"
        admin_password = "Admin@123"  # Change this password!
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            print(f"❌ Admin user already exists: {admin_email}")
            return
        
        # Create admin user
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            phone="+639000000000",
            role="admin",
            is_active=True,
            is_verified=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print(f"⚠️  IMPORTANT: Change this password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
