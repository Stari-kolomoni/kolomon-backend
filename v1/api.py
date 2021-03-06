from fastapi import APIRouter

from .users.users_router import router as users_router
from .users.roles_router import router as roles_router
from .lex.lex_router import router as lex_router


router = APIRouter(
    prefix="/v1"
)

router.include_router(users_router)
router.include_router(roles_router)
router.include_router(lex_router)
