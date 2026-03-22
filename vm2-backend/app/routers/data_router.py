from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CompanyData
from app.schemas import CompanyDataResponse
from app.auth import get_current_user
from app.services.gemini_service import GeminiService

router = APIRouter()
gemini_service = GeminiService()

@router.get("/", response_model=list[CompanyDataResponse])
async def get_company_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get data for the current user's company
    data = db.query(CompanyData).filter(CompanyData.company_id == current_user["company_id"]).all()
    return data

@router.get("/search")
async def search_data(
    query: str,
    current_user: dict = Depends(get_current_user)
):
    # Search files using Gemini service with rsync
    results = await gemini_service.search_files(query, current_user["company_id"])
    return {
        "query": query,
        "company_id": current_user["company_id"],
        "results": results
    }

@router.get("/documents")
async def list_documents(
    current_user: dict = Depends(get_current_user)
):
    # List all documents in the AI Books collection
    results = await gemini_service.search_files("", current_user["company_id"])
    return {
        "message": "List of all available documents",
        "company_id": current_user["company_id"],
        "documents": results
    }
