from datetime import date

from pydantic import BaseModel


class HabitCompletionCreate(BaseModel):
    completed_date: date


class HabitCompletionResponse(BaseModel):
    id: int
    habit_id: int
    completed_date: date

    class Config:
        from_attributes = True