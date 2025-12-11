from sqlalchemy import create_engine
import os

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'vbams')

url = os.getenv('DATABASE_URL', f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print('Using URL:', url)

try:
    engine = create_engine(url, pool_pre_ping=True, future=True)
    with engine.connect() as conn:
        ver = conn.exec_driver_sql('select version()').scalar()
        print('Connected. Server version:', ver)
except Exception as e:
    print('Connection failed:', e)
