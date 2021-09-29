from fastapi import APIRouter
from .categories import router as category_router
from .english_words import router as english_router
from .suggestions import router as suggestions_router
from .links import router as links_router

router = APIRouter(
    prefix='/lex'
)

router.include_router(category_router.router)
router.include_router(english_router.router)
router.include_router(suggestions_router.router)
router.include_router(links_router.router)
