from pydantic import BaseModel, Field


class Related(BaseModel):
    id: int
    lemma: str = Field(alias="word")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
