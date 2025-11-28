from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from .routers import auth, users, documents, ai

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI-Powered Research & Knowledge Hub")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(ai.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Research & Knowledge Hub API"}






