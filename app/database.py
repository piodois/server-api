from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Cadena de conexión a SQL Server con ODBC
if settings.DB_TRUSTED_CONNECTION:
    # Conexión con autenticación de Windows
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{settings.DB_HOST}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
else:
    # Conexión con usuario y contraseña
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

# Creación del motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creación de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()