from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Menu(Base):
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    submenu = relationship('SubMenu', cascade='delete')
