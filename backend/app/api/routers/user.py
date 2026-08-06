from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse,UserLogin,Token
from app.services.user_service import create_user,get_all_users_service,get_user_by_id,login_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
        "/",
        response_model=UserResponse
)

async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db)
):
    return get_all_users_service(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_by_id(db, user_id)

@router.post("/login",response_model=Token)
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(db, user)