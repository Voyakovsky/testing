from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost:5432/educate_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

