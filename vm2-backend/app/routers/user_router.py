from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user, MOCK_USERS

router = APIRouter()

MOCK_COMPANY_NAMES = {
    1: "Acme Corporation",
    2: "Globex Inc.",
    3: "Initech",
    4: "Widget Works",
    5: "Gadget Galaxy"
}

@router.get("/user", response_model=dict)
async def get_user_info(
    current_user: dict = Depends(get_current_user)
):
    username = current_user["username"]
    
    if username not in MOCK_USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = MOCK_USERS[username]
    company_id = user_data["company_id"]
    company_name = MOCK_COMPANY_NAMES.get(company_id, "Unknown Company")
    
    return {
        "user_id": user_data["user_id"],
        "username": username,
        "company_id": company_id,
        "company_name": company_name
    }
