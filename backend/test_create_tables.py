"""
Simple test to create just the database tables
"""
from database import engine
from models import Base

try:
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Success! Tables created.")
    print(f"\nDatabase location: {engine.url}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
