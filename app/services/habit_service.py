from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.habit import Habit


def get_user_habit_or_404(db: Session, habit_id: int, user_id: int) -> Habit:
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    return habit


def get_user_habits(db: Session, user_id: int) -> list[Habit]:
    return (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .all()
    )