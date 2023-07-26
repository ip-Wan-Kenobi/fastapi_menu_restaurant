from pydantic import BaseModel, Field, field_validator


class SubMenuCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str
    menu_id: int


class SubMenuUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str
    menu_id: int

    @field_validator('title', mode='before')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название меню не может быть пустым!')
        return value
