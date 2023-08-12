from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.models import Base

engine = create_engine("sqlite:///platform.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)