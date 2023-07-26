from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.main_menu import (create_main_menu, delete_menu, get_menu_by_id,
                                read_all_menu, update_menu)
from app.schemas.main_menu import MainMenuCreate, MainMenuUpdate

from app.api.validators import check_name_duplicate, check_menu_exists
from app.models import Dish, SubMenu

router = APIRouter(prefix='/api/v1/menus')


@router.post('/')
async def create_new_main_menu(
        main_menu: MainMenuCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(main_menu.title, session)
    new_menu = await create_main_menu(main_menu, session)
    return new_menu


@router.get('/')
async def get_all_menus(
        session: AsyncSession = Depends(get_async_session),
):
    all_menus = await read_all_menu(session)
    for idx, v in enumerate(all_menus):
        count_submenu = await session.execute(select(SubMenu).where(SubMenu.menu_id == v.id))
        count_submenu = count_submenu.scalars().all()
        count_dishes = await session.execute(select(Dish).where(v.id == SubMenu.menu_id)
                                             .where(SubMenu.id == Dish.submenu_id))
        count_dishes = count_dishes.scalars().all()
        all_menus[idx].amount_of_submenus = len(count_submenu)
        all_menus[idx].amount_of_dishes = len(count_dishes)
    return all_menus


@router.get('/{api_test_menu_id}')
async def get_one_menu(
        api_test_menu_id: int,
        session: AsyncSession = Depends(get_async_session),
    ):
    one_menu = await get_menu_by_id(api_test_menu_id, session)
    count_submenu = await session.execute(select(SubMenu).where(SubMenu.menu_id == one_menu.id))
    count_submenu = count_submenu.scalars().all()
    count_dishes = await session.execute(select(Dish).where(one_menu.id == SubMenu.menu_id)
                                         .where(SubMenu.id == Dish.submenu_id))
    count_dishes = count_dishes.scalars().all()
    one_menu.amount_of_submenus = len(count_submenu)
    one_menu.amount_of_dishes = len(count_dishes)
    return one_menu


@router.patch('/{api_test_menu_id}')
async def partially_update_menu(
        api_test_menu_id: int,
        obj_in: MainMenuUpdate,
        session: AsyncSession = Depends(get_async_session),
        ):
    menu = await get_menu_by_id(
        api_test_menu_id, session
    )

    if menu is None:
        raise HTTPException(
            status_code=404,
            detail='Меню не найдено!'
        )

    if obj_in.title is not None:
        await check_name_duplicate(obj_in.title, session)

    menu = await update_menu(
        menu, obj_in, session
    )
    return menu


@router.delete('/{api_test_menu_id}')
async def remove_menu(
        api_test_menu_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await check_menu_exists(api_test_menu_id, session)
    menu = await delete_menu(menu, session)
    return menu
