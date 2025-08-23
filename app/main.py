import os  
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.router import eating, login, playing, sleeping, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dbdbbook.site",
        "http://34.64.82.153:3000",
        "http://34.64.82.153",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어는 따로 추가해야 합니다
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET"),
    max_age=60 * 30,
    same_site="none",
    https_only=True
)

# 기본 라우트
@app.get("/")
def read_root():
    return {"message": "Hi FastAPI!"}

# 라우터 등록
app.include_router(eating.router)
app.include_router(login.router)
app.include_router(playing.router)
app.include_router(sleeping.router)
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
