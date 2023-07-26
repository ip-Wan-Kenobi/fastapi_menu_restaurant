from typing import Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submenu import SubMenu
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate


async def create_submenu(
        new_submenu: SubMenuCreate,
        session: AsyncSession,
        ) -> SubMenu:
    new_submenu_data = new_submenu.model_dump()
    db_submenu = SubMenu(**new_submenu_data)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


async def read_all_submenus(
        session: AsyncSession,
        ) -> list[SubMenu]:
    db_submenus = await session.execute(select(SubMenu))
    return db_submenus.scalars().all()


async def update_submenu(
        db_menu: SubMenu,
        menu_in: SubMenuUpdate,
        session: AsyncSession,
) -> SubMenu:
    obj_data = jsonable_encoder(db_menu)
    update_data = menu_in.model_dump(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_menu, field, update_data[field])
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


async def delete_submenu(
        db_menu: SubMenu,
        session: AsyncSession,
) -> SubMenu:
    await session.delete(db_menu)
    await session.commit()
    return db_menu


async def get_submenu_id_by_name(
        menu_name: str,
        session: AsyncSession,
        ) -> Optional[int]:
    db_menu_id = await session.execute(
        select(SubMenu.id).where(
            SubMenu.title == menu_name
        )
    )
    db_menu_id = db_menu_id.scalars().first()
    return db_menu_id


async def get_submenu_by_id(
        submenu_id: int,
        session: AsyncSession,
) -> Optional[SubMenu]:
    db_menu = await session.get(SubMenu, submenu_id)
    return db_menu
