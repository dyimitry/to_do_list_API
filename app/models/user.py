from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    user_id = Column(Integer)
    first_name = Column(String(100), nullable=False)
    username = Column(String(100))
    last_name = Column(String(100))
    to_do_list = relationship("Task", cascade="delete")

    UniqueConstraint(user_id)
    