from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_submenu_exists, check_name_duplicate_in_dishes, check_dish_exists
)
from app.core.db import get_async_session
from app.crud.dish import (create_dish, delete_dish, get_dish_by_id, read_all_dish, update_dish)
from app.schemas.dish import DishCreate, DishUpdate


router = APIRouter()


@router.post('/dish/')
async def create_new_submenu(
        dish: DishCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate_in_dishes(dish.name, session)
    await check_submenu_exists(dish.submenu_id, session)
    new_dish = await create_dish(dish, session)
    return new_dish


@router.get('/dish/')
async def get_all_submenus(
        session: AsyncSession = Depends(get_async_session)
):
    all_dishes = await read_all_dish(session)
    for idx in range(len(all_dishes)):
        all_dishes[idx].price = round(all_dishes[idx].price, 2)
    return all_dishes


@router.patch('/dish/{dish_id}')
async def partially_update_submenu(
        dish_id: int,
        obj_in: DishUpdate,
        session: AsyncSession = Depends(get_async_session),
        ):
    dish = await get_dish_by_id(
        dish_id, session
    )

    if dish is None:
        raise HTTPException(
            status_code=404,
            detail='Подменю не найдено!'
        )

    if obj_in.name is not None:
        await check_name_duplicate_in_dishes(obj_in.name, session)

    dish = await update_dish(
        dish, obj_in, session
    )
    return dish


@router.delete('/dish/{dish_id}')
async def remove_menu(
        dish_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    dish = await check_dish_exists(dish_id, session)
    dish = await delete_dish(dish, session)
    return dish
