from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ServiceProvider

def delete_users(user_ids):
    db: Session = SessionLocal()
    try:
        print(f"Attempting to delete users with IDs: {user_ids}")
        
        # 1. Delete linked ServiceProvider profiles first (FK constraint)
        providers = db.query(ServiceProvider).filter(ServiceProvider.user_id.in_(user_ids)).all()
        for provider in providers:
            print(f"Deleting ServiceProvider profile for user {provider.user_id} (Provider ID: {provider.id})")
            db.delete(provider)
        
        # Flush to ensure provider deletion is registered before user deletion if cascade isn't set
        db.flush()
        
        # 2. Delete Users
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        for user in users:
            print(f"Deleting User: {user.first_name} {user.last_name} (ID: {user.id})")
            db.delete(user)
            
        db.commit()
        print("Deletion successful.")
        
    except Exception as e:
        print(f"Error during deletion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # IDs from the user's screenshot
    ids_to_delete = [3, 4]
    delete_users(ids_to_delete)
