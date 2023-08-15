import datetime

from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session

import models
import schemas
from database import process_step_db


def add_car_booking(db: Session, car_booking: schemas.CarBookingCreate):
    process_step = process_step_db.get_process_step_by_process_id_and_step(db, 2, 1)
    query = insert(models.CarBooking).values(
        user_id=car_booking.user_id,
        car_id=car_booking.car_id,
        process_step_id=process_step.id,
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
        and_(models.CarBooking.is_deleted == False, models.CarBooking.id == id)).values(
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


def check_available_car(db: Session, car_id: int, start_time: datetime, end_time: datetime):
    process_steps = process_step_db.get_process_steps(db, 1)
    query = select(models.CarBooking).join(models.ProcessStep).where(
        and_(
            models.CarBooking.is_deleted == False,
            models.CarBooking.car_id == car_id,
            models.CarBooking.is_done == True,
            models.ProcessStep.step == process_steps[-1].step,  # last step - completed
            or_(
                models.CarBooking.start_time.between(start_time, end_time),
                models.CarBooking.end_time.between(start_time, end_time),
                and_(models.CarBooking.start_time <= start_time, models.CarBooking.end_time >= end_time)
            )
        )
    )
    print(query)
    result = db.execute(query)
    return result.first() == None
