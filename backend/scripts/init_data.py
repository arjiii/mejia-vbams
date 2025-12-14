from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, UserRole
from auth import get_password_hash
import sys

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

def create_admin_user(db: Session):
    admin_email = "admin@vbams.com"
    admin_pass = "admin123"
    
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if existing_admin:
        print(f"Admin user {admin_email} already exists.")
        return

    print(f"Creating admin user: {admin_email}")
    admin_user = User(
        first_name="Admin",
        last_name="User",
        email=admin_email,
        phone="0000000000",
        hashed_password=get_password_hash(admin_pass),
        role=UserRole.ADMIN,
        is_verified=True,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin user created successfully.")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_pass}")

if __name__ == "__main__":
    try:
        init_db()
        db = SessionLocal()
        create_admin_user(db)
        db.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
