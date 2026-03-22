from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, data_router, chat_router, user_router

app = FastAPI(title="Gemini AI Chatbot Backend", version="1.0.0")

# CORS middleware to allow requests from VM-1 (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(data_router.router, prefix="/api/data", tags=["data"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["chat"])
app.include_router(user_router.router, prefix="/api/data", tags=["data"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Gemini AI Chatbot Backend"}
