import sys
import pathlib
from sqlalchemy import select

# Ensure project root is on sys.path so we can import backend modules
project_root = pathlib.Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# If running from repo root, also include parent
repo_root = pathlib.Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from backend.database import SessionLocal
from backend.models import User


def main():
    with SessionLocal() as db:
        try:
            stmt = select(User).limit(5)
            rows = db.execute(stmt).scalars().all()
            count = db.execute(select(User)).scalars().all()
            print(f"Found up to {len(rows)} users (showing up to 5):\n")
            for u in rows:
                print(f"id={u.id}, email={u.email}, name={u.first_name} {u.last_name}, role={u.role}")
            print(f"\n(Showing up to 5 rows. Total rows fetched earlier for count: {len(count)})")
        except Exception as e:
            print("Error querying users table:", e)


if __name__ == "__main__":
    main()
