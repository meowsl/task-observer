from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization",
                   "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

app.include_router(user_router)
app.include_router(task_router)
