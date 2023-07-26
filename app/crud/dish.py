from typing import Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate


async def create_dish(
        new_dish: DishCreate,
        session: AsyncSession,
        ) -> Dish:
    new_dish_data = new_dish.model_dump()
    db_dish = Dish(**new_dish_data)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


async def read_all_dish(
        session: AsyncSession,
        ) -> list[Dish]:
    db_dish = await session.execute(select(Dish))
    return db_dish.scalars().all()


async def update_dish(
        db_dish: Dish,
        dish_in: DishUpdate,
        session: AsyncSession,
) -> Dish:
    obj_data = jsonable_encoder(db_dish)
    update_data = dish_in.model_dump(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_dish, field, update_data[field])
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


async def delete_dish(
        db_dish: Dish,
        session: AsyncSession,
) -> Dish:
    await session.delete(db_dish)
    await session.commit()
    return db_dish


async def get_dish_id_by_name(
        menu_name: str,
        session: AsyncSession,
        ) -> Optional[int]:
    db_menu_id = await session.execute(
        select(Dish.id).where(
            Dish.name == menu_name
        )
    )
    db_menu_id = db_menu_id.scalars().first()
    return db_menu_id


async def get_dish_by_id(
        dish_id: int,
        session: AsyncSession,
) -> Optional[Dish]:
    db_dish = await session.get(Dish, dish_id)
    return db_dish
