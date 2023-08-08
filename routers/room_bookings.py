#####
##### Room Booking APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from fastapi import APIRouter, HTTPException

from database import room_booking_db, room_db
from dependencies import get_current_user, get_db

router = APIRouter()


# @router.get("/room_bookings/user")
# async def get_room_bookings_by_user(user: schemas.User = Depends(get_current_user),
#                                     db: Session = Depends(get_db)):
#     results = room_booking_db.get_room_bookings_by_user(db, user.id)
#     return results


@router.get("/room_bookings")
async def get_room_bookings_by_user(user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    results = room_booking_db.get_room_bookings_by_role(db, user)
    return results


@router.get("/room_bookings/{id}")
async def get_room_bookings_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    results = room_booking_db.get_room_booking_by_id(db, id)
    return results


# @router.get("/room_bookings/pending")
# async def get_pending_room_booking(user: schemas.User = Depends(get_current_user),
#                               db: Session = Depends(get_db)):
#     if user.role == "manager":
#         return room_booking_db.get_room_bookings_by_status(db, "pending")
#     elif user.role == "hr":
#         return room_booking_db.get_room_bookings_by_status(db, "approved by manager")
#
#
# @router.get("/room_bookings/processed")
# async def get_processed_room_booking(user: schemas.User = Depends(get_current_user),
#                                 db: Session = Depends(get_db)):
#     if user.role == "manager":
#         return room_booking_db.get_room_bookings_by_status(db, "manager")
#     elif user.role == "hr":
#         return room_booking_db.get_room_bookings_by_status(db, "hr")


@router.post("/room_bookings")
async def add_room_booking(room_booking: schemas.RoomBookingCreate, user: schemas.User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    room: models.Room = room_db.get_room_by_id(db, room_booking.room_id)
    if room.capacity < room_booking.participation:
        raise HTTPException(status_code=400, detail="Room does not have enough capacity.")
    if room_booking_db.check_available_room(db, room_booking):
        return room_booking_db.add_room_booking(db, room_booking)
    else:
        raise HTTPException(status_code=400, detail="Room is not available.")


@router.put("/room_bookings/{id}")
async def approve_deny_room_booking(id: int, action: str, user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db),
                                    room_booking: schemas.RoomBookingCreate | None = None):
    if action == "approve":
        db_room_booking = room_booking_db.get_room_booking_by_id(db, id)
        if user.role == "manager" and db_room_booking.status == "pending":
            if room_booking_db.check_available_room(db, db_room_booking):
                return room_booking_db.approve_room_booking(db, id, user.role)
            else:
                raise HTTPException(status_code=400, detail="Room is not available.")
        elif user.role == "hr" and db_room_booking.status == "approved by manager":
            return room_booking_db.approve_room_booking(db, id, user.role)
        else:
            raise HTTPException(status_code=400, detail="Cannot approve.")
    elif action == "deny":
        return room_booking_db.deny_room_booking(db, id, user.role)
    elif action == "update":
        room: models.Room = room_db.get_room_by_id(db, room_booking.room_id)
        if room.capacity < room_booking.participation:
            raise HTTPException(status_code=400, detail="Room does not have enough capacity.")
        if room_booking_db.check_available_room(db, room_booking):
            return room_booking_db.update_room_booking(db, id, room_booking)
        else:
            raise HTTPException(status_code=400, detail="Room is not available.")
