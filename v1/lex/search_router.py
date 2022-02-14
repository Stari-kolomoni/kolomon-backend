from fastapi import APIRouter

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/", status_code=200)
async def search(query: str):
    pass
