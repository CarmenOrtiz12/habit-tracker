from pydantic import BaseModel


class HabitCreate(BaseModel):
    name: str
    description: str | None = None
    frequency: str = "daily"


class HabitResponse(BaseModel):
    id: int
    name: str
    description: str | None
    frequency: str

    class Config:
        from_attributes = True