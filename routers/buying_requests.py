#####
##### Car Booking APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from fastapi import APIRouter, HTTPException

from database import buying_request_db, car_db
from dependencies import get_current_user, get_db

router = APIRouter()


@router.get("/buying_requests")
async def get_buying_requests_by_user(user: schemas.User = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    if user.role == "user":
        results = buying_request_db.get_buying_requests_by_user(db, user)
    else:
        results = buying_request_db.get_buying_requests_by_role(db, user)
    return results


@router.get("/buying_requests/{id}")
async def get_buying_requests_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    return buying_request_db.get_buying_request_by_id(db, id)


@router.post("/buying_requests")
async def add_buying_request(buying_request: schemas.BuyingRequestCreate,
                             user: schemas.User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    return buying_request_db.add_buying_request(db, buying_request)


@router.put("/buying_requests/{id}")
async def buying_request_action(id: int, action: str, user: schemas.User = Depends(get_current_user),
                                db: Session = Depends(get_db),
                                buying_request: schemas.BuyingRequestCreate | None = None):
    db_buying_request = buying_request_db.get_buying_request_by_id(db, id)
    if not db_buying_request:
        raise HTTPException(status_code=400, detail="Buying request not found.")
    if action == "approve":
        return buying_request_db.approve_buying_request(db, id, user)
    elif action == "deny":
        return buying_request_db.deny_buying_request(db, id, user)
    elif action == "update":
        return buying_request_db.update_buying_request(db, id, buying_request)


@router.get("/test")
async def test(db: Session = Depends(get_db)):
    return buying_request_db.test(db)
