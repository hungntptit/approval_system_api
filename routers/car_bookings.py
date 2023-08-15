#####
##### Car Booking APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from fastapi import APIRouter, HTTPException

from database import car_booking_db, car_db, general_request_db
from dependencies import get_current_user, get_db

router = APIRouter()


@router.get("/car_bookings")
async def get_car_bookings_by_user(user: schemas.User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    if user.role == "user":
        results = general_request_db.get_model_by_user(db, user, models.CarBooking)
    else:
        results = general_request_db.get_model_by_role(db, user, models.CarBooking)
    return results


@router.get("/car_bookings/{id}")
async def get_car_bookings_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    results = general_request_db.get_model_by_id(db, id, models.CarBooking)
    return results


@router.post("/car_bookings")
async def add_car_booking(car_booking: schemas.CarBookingCreate, user: schemas.User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    car: models.Car = car_db.get_car_by_id(db, car_booking.car_id)
    print(f"car seats: {car.seats}, nop: {car_booking.number_of_people}")
    if car.seats < car_booking.number_of_people:
        raise HTTPException(status_code=400, detail="Car does not have enough seats.")
    # check = car_booking_db.check_available_car(db, car_booking)
    # print(check)
    if not car_booking_db.check_available_car(db, car_booking.car_id, car_booking.start_time, car_booking.end_time):
        raise HTTPException(status_code=400, detail="Car is not available.")
    else:
        return car_booking_db.add_car_booking(db, car_booking)


@router.put("/car_bookings/{id}")
async def car_booking_action(id: int, action: str, user: schemas.User = Depends(get_current_user),
                             db: Session = Depends(get_db),
                             car_booking: schemas.CarBookingCreate | None = None):
    if action == "approve":
        return general_request_db.approve_model(db, id, user, models.CarBooking)
    elif action == "deny":
        return general_request_db.deny_model(db, id, user, models.CarBooking)
    elif action == "update":
        if user.id != car_booking.user_id:
            raise HTTPException(status_code=400, detail="Not authorized to update car booking")
        car: models.Car = car_db.get_car_by_id(db, car_booking.car_id)
        if car.seats < car_booking.number_of_people:
            raise HTTPException(status_code=400, detail="Car does not have enough seats.")
        if not car_booking_db.check_available_car(db, car_booking.car_id, car_booking.start_time, car_booking.end_time):
            raise HTTPException(status_code=400, detail="Car is not available.")
        else:
            return car_booking_db.update_car_booking(db, id, car_booking)
