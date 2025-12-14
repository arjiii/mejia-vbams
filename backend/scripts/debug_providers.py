
from database import SessionLocal
from models import ServiceProvider
from schemas import ServiceProviderAdminDetail
import json

db = SessionLocal()
try:
    providers = db.query(ServiceProvider).all()
    print(f"Found {len(providers)} providers")
    for p in providers:
        print(f"Provider ID: {p.id}")
        print(f"User ID: {p.user_id}")
        print(f"Services raw: {p.services} (Type: {type(p.services)})")
        print(f"Documents raw: {p.documents} (Type: {type(p.documents)})")
        print(f"User Latitude: {p.user.latitude}")
        
        # Try to validate with Pydantic manually
        try:
            model = ServiceProviderAdminDetail.from_orm(p)
            print("Pydantic Validation: Success")
        except Exception as e:
            print(f"Pydantic Validation Failed: {e}")

except Exception as e:
    print(f"DB Query Failed: {e}")
finally:
    db.close()
