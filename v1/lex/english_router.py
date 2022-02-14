from fastapi import APIRouter

router = APIRouter(
    prefix="/english",
    tags=["English entries"]
)


@router.get("/", status_code=200)
async def read_english_entries():
    pass


@router.post("/", status_code=201)
async def create_english_entry():
    pass


@router.get("/{entry_id}", status_code=200)
async def read_english_entry(entry_id: int):
    pass


@router.put("/{entry_id}", status_code=200)
async def update_english_entry(entry_id: int):
    pass


@router.delete("/entry_id", status_code=200)
async def remove_english_entry(entry_id: int):
    pass
