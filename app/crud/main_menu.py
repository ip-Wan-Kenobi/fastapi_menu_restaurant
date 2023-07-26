from typing import Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.main_menu import Menu
from app.schemas.main_menu import MainMenuCreate, MainMenuUpdate


async def create_main_menu(
        new_menu: MainMenuCreate,
        session: AsyncSession,
        ) -> Menu:
    new_menu_data = new_menu.model_dump()
    db_menu = Menu(**new_menu_data)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


async def read_all_menu(
        session: AsyncSession,
        ) -> list[Menu]:
    db_menus = await session.execute(select(Menu))
    return db_menus.scalars().all()


async def update_menu(
        db_menu: Menu,
        menu_in: MainMenuUpdate,
        session: AsyncSession,
) -> Menu:
    obj_data = jsonable_encoder(db_menu)
    update_data = menu_in.model_dump(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_menu, field, update_data[field])
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


async def delete_menu(
        db_menu: Menu,
        session: AsyncSession,
) -> Menu:
    await session.delete(db_menu)
    await session.commit()
    return db_menu


async def get_menu_id_by_name(
        menu_name: str,
        session: AsyncSession,
        ) -> Optional[int]:
    db_menu_id = await session.execute(
        select(Menu.id).where(
            Menu.title == menu_name
        )
    )
    db_menu_id = db_menu_id.scalars().first()
    return db_menu_id


async def get_menu_by_id(
        menu_id: int,
        session: AsyncSession,
) -> Optional[Menu]:
    db_menu = await session.get(Menu, menu_id)
    return db_menu
