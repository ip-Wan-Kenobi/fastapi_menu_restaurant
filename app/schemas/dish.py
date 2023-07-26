from pydantic import BaseModel, Field, field_validator


class DishCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    price: float = Field(...)
    submenu_id: int


class DishUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    price: float = Field(...)

    @field_validator('name', mode='before')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название меню не может быть пустым!')
        return value
