#####
##### Car Booking APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from fastapi import APIRouter, HTTPException

from database import car_booking_db, car_db
from dependencies import get_current_user, get_db

router = APIRouter()


# @router.get("/car_bookings")
# async def get_car_bookings_by_user(user: schemas.User = Depends(get_current_user),
#                                    db: Session = Depends(get_db)):
#     results = car_booking_db.get_car_bookings_by_user(db, user.id)
#     return results


@router.get("/car_bookings")
async def get_car_bookings_by_user(user: schemas.User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    results = car_booking_db.get_car_bookings_by_role(db, user)
    return results


@router.get("/car_bookings/{id}")
async def get_car_bookings_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    results = car_booking_db.get_car_bookings_by_id(db, id)
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
    if car_booking_db.check_available_car(db, car_booking):
        return car_booking_db.add_car_booking(db, car_booking)
    else:
        raise HTTPException(status_code=400, detail="Car is not available.")


@router.put("/car_bookings/{id}")
async def approve_car_booking(id: int, action: str, user: schemas.User = Depends(get_current_user),
                              db: Session = Depends(get_db), car_booking: schemas.CarBookingCreate | None = None):
    if action == "approve":
        db_car_booking = car_booking_db.get_car_booking_by_id(db, id)
        if user.role == "manager" and db_car_booking.status == "pending":
            if car_booking_db.check_available_car(db, db_car_booking):
                return car_booking_db.approve_car_booking(db, id, user.role)
            else:
                raise HTTPException(status_code=400, detail="Car is not available.")
        elif user.role == "driver" and db_car_booking.status == "approved by manager":
            return car_booking_db.approve_car_booking(db, id, user.role)
        else:
            raise HTTPException(status_code=400, detail="Cannot approve.")
    elif action == "deny":
        return car_booking_db.deny_car_booking(db, id, user.role)
    elif action == "update":
        car: models.Car = car_db.get_car_by_id(db, car_booking.car_id)
        print(f"car seats: {car.seats}, nop: {car_booking.number_of_people}")
        if car.seats < car_booking.number_of_people:
            raise HTTPException(status_code=400, detail="Car does not have enough seats.")
        if car_booking_db.check_available_car(db, car_booking):
            return car_booking_db.update_car_booking(db, id, car_booking)
        else:
            raise HTTPException(status_code=400, detail="Car is not available.")
