import json

import schemas
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session, joinedload

import models


def add_car_booking(db: Session, car_booking: schemas.CarBookingCreate):
    query = insert(models.CarBooking).values(
        user_id=car_booking.user_id,
        car_id=car_booking.car_id,
        title=car_booking.title,
        place=car_booking.place,
        start_time=car_booking.start_time,
        end_time=car_booking.end_time,
        origin=car_booking.origin,
        destination=car_booking.destination,
        distance=car_booking.distance,
        number_of_people=car_booking.number_of_people
    )
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.CarBooking).where(models.CarBooking.id == result.lastrowid)).first()
    return inserted_row


def update_car_booking(db: Session, id: int, car_booking: schemas.CarBookingCreate):
    query = update(models.CarBooking).where(
        (models.CarBooking.is_deleted == False) & (models.CarBooking.id == id)).values(
        user_id=car_booking.user_id,
        car_id=car_booking.car_id,
        title=car_booking.title,
        place=car_booking.place,
        start_time=car_booking.start_time,
        end_time=car_booking.end_time,
        origin=car_booking.origin,
        destination=car_booking.destination,
        distance=car_booking.distance,
        number_of_people=car_booking.number_of_people
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.CarBooking).where(models.CarBooking.id == id)).first()
    return updated_row


def get_car_booking_by_id(db: Session, car_booking_id: int):
    query = select(models.CarBooking).where(
        (models.CarBooking.is_deleted == False) & (models.CarBooking.id == car_booking_id)
    )
    result = db.scalars(query)
    return result.first()


def get_car_bookings_by_user(db: Session, user_id: int):
    query = select(models.CarBooking).where(
        (models.CarBooking.is_deleted == False)
        & (models.CarBooking.user_id == user_id)
    )
    results = db.scalars(query)
    return results.all()


def get_car_bookings_by_role(db: Session, user: schemas.User):
    query = ""
    print(user.role)
    if user.role == "user":
        query = select(models.CarBooking).where(
            (models.CarBooking.is_deleted == False)
            & (models.CarBooking.user_id == user.id))
    elif user.role == "manager":
        query = select(models.CarBooking).where(
            (models.CarBooking.is_deleted == False)
            & (models.CarBooking.status.like("%pending%") | models.CarBooking.status.like("%manager%"))
        )
    elif user.role == "driver":
        query = select(models.CarBooking).where(
            (models.CarBooking.is_deleted == False)
            & (models.CarBooking.status.like("%approved by manager%") | models.CarBooking.status.like("%driver%"))
        )

    results = db.scalars(query)
    return results.all()


def get_car_bookings_by_status(db: Session, status: str):
    query = select(models.CarBooking).where(
        (models.CarBooking.is_deleted == False)
        & models.CarBooking.status.like(f"%{status}%")
    )
    result = db.scalars(query)
    return result.all()


def approve_car_booking(db: Session, car_booking_id: int, role: str):
    query = update(models.CarBooking).where(
        (models.CarBooking.is_deleted == False)
        & (models.CarBooking.id == car_booking_id)
    ).values(
        status="approved by " + role)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.CarBooking).where(models.CarBooking.id == car_booking_id)).first()
    return updated_row


def deny_car_booking(db: Session, car_booking_id: int, role: str):
    query = update(models.CarBooking).where(
        (models.CarBooking.is_deleted == False)
        & (models.CarBooking.id == car_booking_id)
    ).values(
        status="denied by " + role)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.CarBooking).where(models.CarBooking.id == car_booking_id)).first()
    return updated_row


def check_available_car(db: Session, car_booking: schemas.CarBookingCreate):
    car_id = car_booking.car_id
    start_time = car_booking.start_time
    end_time = car_booking.end_time
    query = select(models.CarBooking).where(
        (models.CarBooking.is_deleted == False) &
        (models.CarBooking.car_id == car_id) &
        (models.CarBooking.status.like("%approved%")) &
        (
            (models.CarBooking.start_time.between(start_time, end_time) |
             (models.CarBooking.end_time.between(start_time, end_time) |
              (
                      (models.CarBooking.start_time <= start_time) &
                      (models.CarBooking.end_time >= end_time))
              ))
        )
    )
    print(query)
    result = db.execute(query)
    return result.first() == None
