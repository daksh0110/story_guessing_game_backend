from app.db import Base, engine
from app.models.user import User
from app.models.player import Player
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
