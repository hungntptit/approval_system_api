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
    results = buying_request_db.get_buying_requests_by_role(db, user)
    return results


@router.get("/buying_requests/{id}")
async def get_buying_requests_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    results = buying_request_db.get_buying_request_by_id(db, id)
    return results


@router.post("/buying_requests")
async def add_buying_request(buying_request: schemas.BuyingRequestCreate,
                             user: schemas.User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    return buying_request_db.add_buying_request(db, buying_request)


@router.put("/buying_requests/{id}")
async def approve_buying_request(id: int, action: str, user: schemas.User = Depends(get_current_user),
                                 db: Session = Depends(get_db),
                                 buying_request: schemas.BuyingRequestCreate | None = None):
    db_buying_request = buying_request_db.get_buying_request_by_id(db, id)
    current_status = db_buying_request.status
    next_status = current_status
    if action == "approve":
        if ((user.role == "manager" and db_buying_request.status == "pending") |
                (user.role == "tech" and db_buying_request.status == "approved by hr")):
            next_status = "approved by " + user.role
        elif user.role == "hr":
            if db_buying_request.status == "approved by manager":
                next_status = "approved by " + user.role
            elif db_buying_request.status == "approved by tech":
                next_status = "buying"
            elif db_buying_request.status == "buying":
                next_status = "completed"
        else:
            raise HTTPException(status_code=400, detail="Cannot approve.")
        return buying_request_db.set_buying_request_status(db, id, next_status)
    elif action == "deny":
        return buying_request_db.set_buying_request_status(db, id, "denied by " + user.role)
    elif action == "update":
        return buying_request_db.update_buying_request(db, id, buying_request)


@router.get("/test")
async def test(db: Session = Depends(get_db)):
    return buying_request_db.test(db)