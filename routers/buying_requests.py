#####
##### Car Booking APIs
#####
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import buying_request_db, general_request_db
from dependencies import get_current_user, get_db

router = APIRouter()


@router.get("/buying_requests")
async def get_buying_requests_by_user(user: schemas.User = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    if user.role == "user":
        results = general_request_db.get_model_by_user(db, user, models.BuyingRequest)
    else:
        results = general_request_db.get_model_by_role(db, user, models.BuyingRequest)
    return results


@router.get("/buying_requests/{id}")
async def get_buying_requests_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    return general_request_db.get_model_by_id(db, id, models.BuyingRequest)


@router.post("/buying_requests")
async def add_buying_request(buying_request: schemas.BuyingRequestCreate,
                             user: schemas.User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    if user.role != "user":
        raise HTTPException(status_code=400, detail="Not authorized to add buying request")
    return buying_request_db.add_buying_request(db, buying_request)


@router.put("/buying_requests/{id}")
async def buying_request_action(id: int, action: str, user: schemas.User = Depends(get_current_user),
                                db: Session = Depends(get_db),
                                buying_request: schemas.BuyingRequestCreate | None = None):
    db_buying_request = general_request_db.get_model_by_id(db, id, models.BuyingRequest)
    if not db_buying_request:
        raise HTTPException(status_code=400, detail="Buying request not found.")
    if action == "approve":
        return general_request_db.approve_model(db, id, user, models.BuyingRequest)
    elif action == "deny":
        return general_request_db.deny_model(db, id, user, models.BuyingRequest)
    elif action == "update":
        if user.id != db_buying_request.user_id:
            raise HTTPException(status_code=400, detail="Not authorized to update buying request")
        return buying_request_db.update_buying_request(db, id, buying_request)
