from fastapi import APIRouter

router = APIRouter(
    prefix="/slovene",
    tags=["Slovene entries"]
)


@router.get("/", status_code=200)
async def read_slovene_entries():
    pass


@router.post("/", status_code=201)
async def create_slovene_entry():
    pass


@router.get("/{entry_id}", status_code=200)
async def read_slovene_entry(entry_id: int):
    pass


@router.put("/{entry_id}", status_code=200)
async def update_slovene_entry(entry_id: int):
    pass


@router.delete("/entry_id", status_code=200)
async def remove_slovene_entry(entry_id: int):
    pass
