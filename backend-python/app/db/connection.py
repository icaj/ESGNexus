from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

@contextmanager
def get_connection():
    """Abre uma conexao PostgreSQL/NeonDB.

    Para NeonDB, prefira usar DATABASE_URL no .env, por exemplo:
    postgresql://usuario:senha@ep-xxxx.us-east-2.aws.neon.tech/esg_nexus?sslmode=require
    """
    if settings.database_url:
        conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
    else:
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            sslmode=settings.db_sslmode,
            cursor_factory=RealDictCursor,
        )
    conn.autocommit = False
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
