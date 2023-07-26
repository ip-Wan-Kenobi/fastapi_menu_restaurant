from fastapi import APIRouter

from app.api.endpoints import main_menu_router, submenu_router, dish_router

main_router = APIRouter()
main_router.include_router(main_menu_router, tags=['Main menu'])
main_router.include_router(submenu_router, tags=['Submenu'])
main_router.include_router(dish_router, tags=['Dish'])

