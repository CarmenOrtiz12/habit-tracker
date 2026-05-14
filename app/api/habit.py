from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate, HabitTodayResponse
from app.models.habit_completion import HabitCompletion
from app.schemas.habit_completion import (
    HabitCompletionCreate,
    HabitCompletionResponse,
)

router = APIRouter()


@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_habit = Habit(
        name=habit.name,
        description=habit.description,
        frequency=habit.frequency,
        user_id=current_user.id,
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)

    return db_habit


@router.get("/habits", response_model=list[HabitResponse])
def get_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habits = (
        db.query(Habit)
        .filter(Habit.user_id == current_user.id)
        .all()
    )

    return habits


@router.post("/habits/{habit_id}/complete", response_model=HabitCompletionResponse,
status_code=status.HTTP_201_CREATED)
def complete_habit(habit_id: int, completion: HabitCompletionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )
    
    existing_completion = (
        db.query(HabitCompletion)
        .filter(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.completed_date == completion.completed_date,
        )
        .first()
    )

    if existing_completion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este hábito ya fue marcado como completado en esta fecha",
        )

    habit_completion = HabitCompletion(
        habit_id=habit.id,
        completed_date=completion.completed_date,
    )

    db.add(habit_completion)
    db.commit()
    db.refresh(habit_completion)

    return habit_completion


@router.get("/habits/today", response_model=list[HabitTodayResponse])
def get_today_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()

    habits = (
        db.query(Habit)
        .filter(Habit.user_id == current_user.id)
        .all()
    )

    response = []

    for habit in habits:
        completion = (
            db.query(HabitCompletion)
            .filter(
                HabitCompletion.habit_id == habit.id,
                HabitCompletion.completed_date == today,
            )
            .first()
        )

        response.append(
            HabitTodayResponse(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=habit.frequency,
                completed_today=completion is not None,
                completed_date=completion.completed_date if completion else None,
            )
        )

    return response


@router.get("/habits/{habit_id}/completions", response_model=list[HabitCompletionResponse])
def get_habit_completions(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    completions = (
        db.query(HabitCompletion)
        .filter(HabitCompletion.habit_id == habit.id)
        .order_by(HabitCompletion.completed_date.desc())
        .all()
    )

    return completions


@router.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    return habit


@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    habit.name = habit_data.name
    habit.description = habit_data.description
    habit.frequency = habit_data.frequency

    db.commit()
    db.refresh(habit)

    return habit


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    db.delete(habit)
    db.commit()