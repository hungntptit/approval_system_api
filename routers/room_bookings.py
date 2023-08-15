#####
##### Room Booking APIs
#####
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import room_booking_db, room_db, general_request_db
from dependencies import get_current_user, get_db

router = APIRouter()


@router.get("/room_bookings")
async def get_room_bookings_by_user(user: schemas.User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    if user.role == "user":
        results = general_request_db.get_model_by_user(db, user, models.RoomBooking)
    else:
        results = general_request_db.get_model_by_role(db, user, models.RoomBooking)
    return results


@router.get("/room_bookings/{id}")
async def get_room_bookings_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                  db: Session = Depends(get_db)):
    results = general_request_db.get_model_by_id(db, id, models.RoomBooking)
    return results


@router.post("/room_bookings")
async def add_room_booking(room_booking: schemas.RoomBookingCreate, user: schemas.User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    room: models.Room = room_db.get_room_by_id(db, room_booking.room_id)
    if room.capacity < room_booking.participation:
        raise HTTPException(status_code=400, detail="Room does not have enough capacity.")
    if not room_booking_db.check_available_room(db, room_booking.room_id, room_booking.booking_date,
                                                room_booking.start_time, room_booking.end_time):
        raise HTTPException(status_code=400, detail="Room is not available.")
    else:
        return room_booking_db.add_room_booking(db, room_booking)


@router.put("/room_bookings/{id}")
async def room_booking_action(id: int, action: str, user: schemas.User = Depends(get_current_user),
                              db: Session = Depends(get_db),
                              room_booking: schemas.RoomBookingCreate | None = None):
    if action == "approve":
        return general_request_db.approve_model(db, id, user, models.RoomBooking)
    elif action == "deny":
        return general_request_db.deny_model(db, id, user, models.RoomBooking)
    elif action == "update":
        if user.id != room_booking.user_id:
            raise HTTPException(status_code=400, detail="Not authorized to update room booking")
        room: models.Room = room_db.get_room_by_id(db, room_booking.room_id)
        if room.capacity < room_booking.participation:
            raise HTTPException(status_code=400, detail="Room does not have enough capacity.")
        if not room_booking_db.check_available_room(db, room_booking.room_id, room_booking.booking_date,
                                                    room_booking.start_time, room_booking.end_time):
            raise HTTPException(status_code=400, detail="Room is not available.")
        else:
            raise HTTPException(status_code=400, detail="Room is not available.")
