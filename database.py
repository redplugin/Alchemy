from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:scar@localhost:5432/darmen_test_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
