
from database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
if inspector.has_table("service_providers"):
    print("Table 'service_providers' exists.")
    columns = [c['name'] for c in inspector.get_columns("service_providers")]
    print(f"Columns: {columns}")
else:
    print("Table 'service_providers' DOES NOT exist.")
