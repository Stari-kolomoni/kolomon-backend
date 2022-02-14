from fastapi import APIRouter
from .english_router import router as english_router
from .slovene_router import router as slovene_router
from .links_router import router as links_router
from .search_router import router as search_router
from .entry_router import router as entry_router


router = APIRouter(
    prefix="/lex",
    tags=[]
)

router.include_router(english_router)
router.include_router(slovene_router)
router.include_router(links_router)
router.include_router(search_router)
router.include_router(entry_router)
