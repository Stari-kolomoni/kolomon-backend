from fastapi import APIRouter
from .entry_router import router as entry_router
from .translation_state_router import router as ts_router
from .category_router import router as category_router

router = APIRouter(
    prefix="/lex",
    tags=[]
)

router.include_router(entry_router)
router.include_router(ts_router)
router.include_router(category_router)
