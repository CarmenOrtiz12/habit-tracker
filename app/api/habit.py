from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import (
    HabitCreate,
    HabitResponse,
    HabitUpdate,
    HabitTodayResponse,
    HabitStatsResponse,
)
from app.models.habit_completion import HabitCompletion
from app.schemas.habit_completion import (
    HabitCompletionCreate,
    HabitCompletionResponse,
)
from .utils import calculate_streak
from app.services.habit_service import get_user_habit_or_404, get_user_habits

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
    habits = get_user_habits(db=db, user_id=current_user.id)
    return habits


@router.post("/habits/{habit_id}/complete", response_model=HabitCompletionResponse,
status_code=status.HTTP_201_CREATED)
def complete_habit(habit_id: int, completion: HabitCompletionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)

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


@router.post("/habits/{habit_id}/complete-today", response_model=HabitCompletionResponse,  status_code=status.HTTP_201_CREATED)
def complete_habit_today(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)

    existing_completion = (
        db.query(HabitCompletion)
        .filter(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.completed_date == today,
        )
        .first()
    )

    if existing_completion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este hábito ya fue marcado como completado hoy",
        )

    habit_completion = HabitCompletion(
        habit_id=habit.id,
        completed_date=today,
    )

    db.add(habit_completion)
    db.commit()
    db.refresh(habit_completion)

    return habit_completion


@router.get("/habits/today", response_model=list[HabitTodayResponse])
def get_today_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    habits = get_user_habits(db=db, user_id=current_user.id)
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

        all_completions = (
            db.query(HabitCompletion)
            .filter(HabitCompletion.habit_id == habit.id)
            .all()
        )

        streak = calculate_streak(all_completions)

        response.append(
            HabitTodayResponse(
                id=habit.id,
                name=habit.name,
                description=habit.description,
                frequency=habit.frequency,
                completed_today=completion is not None,
                completed_date=completion.completed_date if completion else None,
                streak=streak,
            )
        )

    return response


@router.get("/habits/stats", response_model=HabitStatsResponse)
def get_habit_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    habits = get_user_habits(db=db, user_id=current_user.id)
    total_habits = len(habits)

    completed_today = (
        db.query(HabitCompletion)
        .join(Habit)
        .filter(
            Habit.user_id == current_user.id,
            HabitCompletion.completed_date == today,
        )
        .count()
    )

    return HabitStatsResponse(
        total_habits=total_habits,
        completed_today=completed_today,
        pending_today=total_habits - completed_today,
    )


@router.get("/habits/{habit_id}/completions", response_model=list[HabitCompletionResponse])
def get_habit_completions(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)

    completions = (
        db.query(HabitCompletion)
        .filter(HabitCompletion.habit_id == habit.id)
        .order_by(HabitCompletion.completed_date.desc())
        .all()
    )

    return completions


@router.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)
    return habit


@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)

    habit.name = habit_data.name
    habit.description = habit_data.description
    habit.frequency = habit_data.frequency

    db.commit()
    db.refresh(habit)

    return habit


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = get_user_habit_or_404(db=db, habit_id=habit_id, user_id=current_user.id)

    db.delete(habit)
    db.commit()