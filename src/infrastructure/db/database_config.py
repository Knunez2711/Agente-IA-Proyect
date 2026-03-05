"""
Infrastructure: Database Configuration
Gestión de la conexión a PostgreSQL con SQLAlchemy.
"""
import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    return (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


def create_db_engine() -> Engine:
    """Crea el engine de SQLAlchemy con connection pooling."""
    return create_engine(
        get_database_url(),
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,   # Verifica conexiones antes de usarlas
        echo=False,
    )