from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.schemas.user import UserCreate
from app.database.dependencies import get_db
from app.models.user import User
from app.core.security import hash_password


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
    }