from fastapi import APIRouter
from .entry_router import router as entry_router


router = APIRouter(
    prefix="/lex",
    tags=[]
)

router.include_router(entry_router)
