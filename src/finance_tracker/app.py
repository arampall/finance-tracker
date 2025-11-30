from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import transactions, users

app = FastAPI(
    title="Finance Tracker API",
    description="API for tracking personal finances",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Finance Tracker API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }