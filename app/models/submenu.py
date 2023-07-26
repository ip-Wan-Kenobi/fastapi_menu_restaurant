from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class SubMenu(Base):
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    dish = relationship('Dish', cascade='delete')

