import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.google_auth import router as google_auth_router
from app.routers.email_auth import router as email_auth_router
from app.routers.gmail_auth import router as gmail_auth_router
from app.routers.password_reset import router as password_reset_router

load_dotenv()

app = FastAPI(
    title="KAVERI AI Authentication API",
    description="Secure Authentication System",
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    same_site="lax",
    https_only=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(google_auth_router)
app.include_router(email_auth_router)
app.include_router(gmail_auth_router)
app.include_router(password_reset_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to KAVERI AI Authentication API",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


