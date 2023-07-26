from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text

from app.core.db import Base


class Dish(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float(precision=10), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenu.id'))

