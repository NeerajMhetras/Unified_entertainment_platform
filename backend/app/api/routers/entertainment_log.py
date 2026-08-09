from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.entertainment_log import (
    EntertainmentLogCreate,
    EntertainmentLogResponse,
    EntertainmentLogUpdate
)
from app.models.entertainment_log import EntertainmentLog
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/logs",
    tags=["Entertainment Logs"]
)


@router.post(
    "/",
    response_model=EntertainmentLogResponse
)
def create_log(
    log_data: EntertainmentLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_log = EntertainmentLog(
        user_id=current_user.id,
        entertainment_id=log_data.entertainment_id,
        rating=log_data.rating,
        review=log_data.review,
        logged_at=log_data.logged_at
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


@router.get(
    "/",
    response_model=list[EntertainmentLogResponse]
)
def get_my_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(EntertainmentLog).filter(
        EntertainmentLog.user_id == current_user.id
    ).all()

    return logs



@router.get(
    "/{log_id}",
    response_model=EntertainmentLogResponse
)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(EntertainmentLog).filter(
        EntertainmentLog.id == log_id,
        EntertainmentLog.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return log

@router.put(
    "/{log_id}",
    response_model=EntertainmentLogResponse
)
def update_log(
    log_id: int,
    log_data: EntertainmentLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(EntertainmentLog).filter(
            EntertainmentLog.id == log_id,
            EntertainmentLog.user_id == current_user.id
        ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )
    if "rating" in log_data.model_fields_set:
        log.rating = log_data.rating

    if "review" in log_data.model_fields_set:
        log.review = log_data.review

    if "logged_at" in log_data.model_fields_set:
        log.logged_at = log_data.logged_at

    db.commit()
    db.refresh(log)

    return log


@router.delete("/{log_id}")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(EntertainmentLog).filter(
        EntertainmentLog.id == log_id,
        EntertainmentLog.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Log deleted successfully"
    }