from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import inspect
from server.config import (
    ORIGINS,
    Base,
    engine,
    SECRET_KEY,
    get_db,
    SQLALCHEMY_DATABASE_URL
)
from server.routes import (
    user_router,
    task_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    root_path="/api/v1",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://185.211.170.161",
    "http://185.211.170.161:80",
    "http://185.211.170.161:8080",
    "http://0.0.0.0:80",
    "http://0.0.0.0:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

app.include_router(user_router)
app.include_router(task_router)
