from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Habit Tracker API funcionando 🚀"}