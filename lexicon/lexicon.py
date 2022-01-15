from fastapi import APIRouter
from .categories import router as category_router
from .english_words import router as english_router
from .suggestions import router as suggestions_router
from .links import router as links_router
from .related import router as related_router
from .slovene_words import router as slovene_router
from .translations import router as translation_router
from .other import router as other_router
from .search import router as search_router

router = APIRouter(
    prefix='/lex'
)

router.include_router(category_router.router)
router.include_router(english_router.router)
router.include_router(suggestions_router.router)
router.include_router(links_router.router)
router.include_router(related_router.router)
router.include_router(slovene_router.router)
router.include_router(translation_router.router)
router.include_router(other_router.router)
router.include_router(search_router.router)
