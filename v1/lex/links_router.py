from fastapi import APIRouter

router = APIRouter(
    prefix="/links",
    tags=["Links"]
)


@router.post("/", status_code=201)
async def create_link():
    pass
