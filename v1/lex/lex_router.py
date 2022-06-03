from fastapi import APIRouter
from .entry_router import router as entry_router
from .translation_state_router import router as ts_router

router = APIRouter(
    prefix="/lex",
    tags=[]
)

router.include_router(entry_router)
router.include_router(ts_router)
