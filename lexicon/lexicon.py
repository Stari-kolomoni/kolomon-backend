from fastapi import APIRouter
from .categories import router as category_router
from .english_words import router as english_router

router = APIRouter(
    prefix='/lex'
)

router.include_router(category_router.router)
router.include_router(english_router.router)
