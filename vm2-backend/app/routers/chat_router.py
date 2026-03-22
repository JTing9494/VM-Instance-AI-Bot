from fastapi import APIRouter, Depends, HTTPException, status
from app.services.gemini_service import GeminiService
from app.auth import get_current_user

router = APIRouter()

DOCUMENT_KEYWORDS = ["document", "file", "book", "pdf", "ai book", "list", "what do i have", "access to"]

@router.post("")
async def chat(
    message: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat endpoint that uses Gemini AI with company-scoped context and document search
    """
    user_message = message.get("message", "").lower()
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )
    
    # Initialize Gemini service
    gemini_service = GeminiService()
    
    # Check if user is asking about documents
    context_data = []
    if any(keyword in user_message for keyword in DOCUMENT_KEYWORDS):
        documents = await gemini_service.search_files(user_message, current_user["company_id"])
        for doc in documents:
            context_data.append({
                "key": doc["filename"],
                "value": doc["snippet"]
            })
    
    # Generate response using Gemini
    response = await gemini_service.generate_content(message.get("message", ""), context_data)
    
    return {"response": response}
