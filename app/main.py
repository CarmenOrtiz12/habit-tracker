from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.habit import router as habit_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(habit_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173,"
        "https://habit-tracker-web-steel.vercel.app,"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API funcionando 🚀"}