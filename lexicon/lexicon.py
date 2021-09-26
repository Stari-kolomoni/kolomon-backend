from fastapi import APIRouter
from .categories import router as category_router

router = APIRouter(
    prefix='/lex'
)

router.include_router(category_router.router)
