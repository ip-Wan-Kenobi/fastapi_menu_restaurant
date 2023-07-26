from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_menu_exists, check_name_duplicate_in_submanu
)
from app.core.db import get_async_session
from app.crud.submenu import (create_submenu, delete_submenu,
                              get_submenu_by_id, read_all_submenus, update_submenu)
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate
from app.models import Dish

router = APIRouter(prefix='/api/v1/menus/{api_test_menu_id}')


@router.post('/submenus')
async def create_new_submenu(
        api_test_submenu_id: SubMenuCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate_in_submanu(api_test_submenu_id.title, session)
    await check_menu_exists(api_test_submenu_id.menu_id, session)
    new_submenu = await create_submenu(api_test_submenu_id, session)
    return new_submenu


@router.get('/submenus')
async def get_all_submenus(
        session: AsyncSession = Depends(get_async_session)
):
    all_submenus = await read_all_submenus(session)
    for idx, v in enumerate(all_submenus):
        count_dishes = await session.execute(select(Dish).where(v.id == Dish.submenu_id))
        count_dishes = count_dishes.scalars().all()
        all_submenus[idx].amount_of_dishes = len(count_dishes)
    return all_submenus


@router.get('/submenus/{api_test_submenu_id}')
async def get_one_menu(
        api_test_submenu_id: int,
        session: AsyncSession = Depends(get_async_session),
    ):
    one_submenu = await get_submenu_by_id(api_test_submenu_id, session)
    count_dishes = await session.execute(select(Dish).where(one_submenu.id == Dish.submenu_id))
    count_dishes = count_dishes.scalars().all()
    one_submenu.amount_of_dishes = len(count_dishes)
    return one_submenu


@router.patch('/submenus/{api_test_submenu_id}')
async def partially_update_submenu(
        api_test_menu_id: int,
        api_test_submenu_id: int,
        obj_in: SubMenuUpdate,
        session: AsyncSession = Depends(get_async_session),
        ):
    submenu = await get_submenu_by_id(
        api_test_submenu_id, session
    )

    if submenu is None:
        raise HTTPException(
            status_code=404,
            detail='Подменю не найдено!'
        )

    if obj_in.title is not None:
        await check_name_duplicate_in_submanu(obj_in.title, session)

    submenu = await update_submenu(
        submenu, obj_in, session
    )
    return submenu


@router.delete('/submenus/{api_test_submenu_id}')
async def remove_menu(
        api_test_submenu_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = await check_menu_exists(api_test_submenu_id, session)
    submenu = await delete_submenu(submenu, session)
    return submenu
