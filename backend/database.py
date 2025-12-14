from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
# For development, we'll use SQLite
# In production, can switch to DATABASE_URL env var for PostgreSQL/MySQL
USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"

if USE_SQLITE:
    # SQLite database file will be created in the backend folder
    SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "vbams.db")
    DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
    # SQLite specific settings
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=False  # Set to True for SQL query logging
    )
else:
    # MySQL/PostgreSQL configuration
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        # Fallback to MySQL components if full URL not provided
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
        DB_PORT = os.getenv("DB_PORT", "3306")
        DB_NAME = os.getenv("DB_NAME", "vbams")
        
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Standard DB Engine
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for models
Base = declarative_base()


def get_db():
    """Yield a database session for dependency injection.
    
    Example usage in FastAPI routes:
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database by creating all tables."""
    from models import Base  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DATABASE_URL}")
