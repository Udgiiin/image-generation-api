from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    rounds = Column(String, nullable=False)