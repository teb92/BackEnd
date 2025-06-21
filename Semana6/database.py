from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Replace with your PostgreSQL credentials and database
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

# Create engine
engine = create_engine(DATABASE_URL)

# Declare base class for models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(bind=engine)