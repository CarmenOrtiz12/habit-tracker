from pydantic import BaseModel
from datetime import date


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


class HabitUpdate(BaseModel):
    name: str
    description: str | None = None
    frequency: str


class HabitTodayResponse(BaseModel):
    id: int
    name: str
    description: str | None
    frequency: str
    completed_today: bool
    completed_date: date | None = None
    streak: int