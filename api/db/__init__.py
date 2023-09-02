from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.models.base import Base

engine = create_engine("sqlite:///api/db/platform.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
