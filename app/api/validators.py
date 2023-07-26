from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.main_menu import get_menu_id_by_name, get_menu_by_id
from app.crud.submenu import get_submenu_id_by_name, get_submenu_by_id
from app.crud.dish import get_dish_id_by_name, get_dish_by_id

from app.models.main_menu import Menu


async def check_name_duplicate(
        menu_name: str,
        session: AsyncSession,
        ) -> None:
    menu_id = await get_menu_id_by_name(menu_name, session)
    if menu_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Меню с таким именем уже существует!',
        )
    return menu_id


async def check_menu_exists(
        menu_id: int,
        session: AsyncSession,
) -> Menu:
    menu = await get_menu_by_id(menu_id, session)
    if menu is None:
        raise HTTPException(
            status_code=404,
            detail='Меню не найдено!'
        )
    return menu


async def check_dish_exists(
       dish_id: int,
        session: AsyncSession,
) -> Menu:
    dish = await get_dish_by_id(dish_id, session)
    if dish is None:
        raise HTTPException(
            status_code=404,
            detail='Блюдо не найдено!'
        )
    return dish


async def check_name_duplicate_in_submanu(
        menu_name: str,
        session: AsyncSession,
        ) -> None:
    menu_id = await get_submenu_id_by_name(menu_name, session)
    if menu_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Подменю с таким именем уже существует!',
        )
    return menu_id


async def check_name_duplicate_in_dishes(
        dish_name: str,
        session: AsyncSession,
        ) -> None:
    dish_id = await get_dish_id_by_name(dish_name, session)
    if dish_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Блюдо с таким именем уже существует!',
        )
    return dish_id


async def check_submenu_exists(
        menu_id: int,
        session: AsyncSession,
) -> Menu:
    menu = await get_submenu_by_id(menu_id, session)
    if menu is None:
        raise HTTPException(
            status_code=404,
            detail='Подменю не найдено!'
        )
    return menu
