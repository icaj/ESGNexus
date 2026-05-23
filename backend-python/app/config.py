import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name: str = os.getenv('APP_NAME', 'ESG Nexus API Python - NeonDB PostgreSQL')
    host: str = os.getenv('APP_HOST', '0.0.0.0')
    port: int = int(os.getenv('APP_PORT', '8080'))

    # Recomendado para NeonDB:
    # postgresql://usuario:senha@ep-xxxx.us-east-2.aws.neon.tech/esg_nexus?sslmode=require
    database_url: str = os.getenv('DATABASE_URL', '')

    # Fallback para PostgreSQL local, caso DATABASE_URL nao seja informado
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = int(os.getenv('DB_PORT', '5432'))
    db_name: str = os.getenv('DB_NAME', 'esg_nexus')
    db_user: str = os.getenv('DB_USER', 'esg_user')
    db_password: str = os.getenv('DB_PASSWORD', 'esg_pass')
    db_sslmode: str = os.getenv('DB_SSLMODE', 'require')

    token_expiration_minutes: int = int(os.getenv('TOKEN_EXPIRATION_MINUTES', '480'))

settings = Settings()
