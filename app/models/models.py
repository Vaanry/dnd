from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func

from app.core.config import Base


class Users(Base):
    reg_date = Column(DateTime(timezone=False), server_default=func.now())
    username = Column(String, unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
