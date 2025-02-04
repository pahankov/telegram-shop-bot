from sqlalchemy import create_engine
from database.models import Base
from config import Config

engine = create_engine(Config.DB_URL)
Base.metadata.create_all(engine)
print("Database tables created!")
