
from database import engine
from sqlalchemy import text, inspect

def run_migration():
    inspector = inspect(engine)
    if not inspector.has_table("service_providers"):
        print("Table 'service_providers' missing. Creation should be handled by create_all.")
        return

    columns = [c['name'] for c in inspector.get_columns("service_providers")]
    print(f"Existing columns: {columns}")

    with engine.connect() as conn:
        # Check and add 'services'
        if 'services' not in columns:
            print("Adding 'services' column...")
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN services TEXT"))
        
        if 'documents' not in columns:
            print("Adding 'documents' column...")
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN documents TEXT"))
        
        if 'is_online' not in columns:
            print("Adding 'is_online' column...")
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN is_online BOOLEAN DEFAULT FALSE"))
            
        if 'base_rate' not in columns:
            print("Adding 'base_rate' column...")
            # Set default 0.0 to avoid NOT NULL violation if rows exist
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN base_rate FLOAT DEFAULT 500.0"))
            
        if 'latitude' not in columns:
             print("Adding 'latitude' column...")
             conn.execute(text("ALTER TABLE service_providers ADD COLUMN latitude FLOAT DEFAULT 0.0"))

        if 'longitude' not in columns:
             print("Adding 'longitude' column...")
             conn.execute(text("ALTER TABLE service_providers ADD COLUMN longitude FLOAT DEFAULT 0.0"))
             
        if 'business_license' not in columns:
            print("Adding 'business_license' column...")
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN business_license VARCHAR(50)"))
            
        if 'business_name' not in columns:
            print("Adding 'business_name' column...")
            conn.execute(text("ALTER TABLE service_providers ADD COLUMN business_name VARCHAR(100)"))

        if 'average_rating' not in columns:
             conn.execute(text("ALTER TABLE service_providers ADD COLUMN average_rating FLOAT DEFAULT 0.0"))
             
        if 'rating_count' not in columns:
             conn.execute(text("ALTER TABLE service_providers ADD COLUMN rating_count INTEGER DEFAULT 0"))

        conn.commit()
        print("Schema update complete.")

if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"Migration Failed: {e}")
