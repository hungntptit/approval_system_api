import datetime
import json

from fastapi import HTTPException

import schemas
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session, joinedload

import models
from database import process_step_db, general_request_db


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


def convert_result_to_car_booking(result):
    ls = []
    for car_booking in result:
        rb = models.CarBooking(
            id=car_booking.id,
            user_id=car_booking.user_id,
            car_id=car_booking.car_id,
            process_step_id=car_booking.process_step_id,
            title=car_booking.title,
            place=car_booking.place,
            start_time=car_booking.start_time,
            end_time=car_booking.end_time,
            origin=car_booking.origin,
            destination=car_booking.destination,
            distance=car_booking.distance,
            number_of_people=car_booking.number_of_people,
            created_at=car_booking.created_at,
            updated_at=car_booking.updated_at,
            status=car_booking.status,
            is_done=car_booking.is_done,
            is_deleted=car_booking.is_deleted,

            car=car_booking.car,
            process_step=car_booking.process_step
        )
        ls.append(rb)
    return ls


def approve_car_booking(db: Session, car_booking_id: int, user: schemas.User):
    db_car_booking = general_request_db.get_model_by_id(db, car_booking_id, models.CarBooking)
    if db_car_booking.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to approve")
    elif db_car_booking.is_done:
        raise HTTPException(status_code=400, detail="Room booking have already denied or completed")
    elif db_car_booking.start_time < datetime.datetime.now().time():
        raise HTTPException(status_code=400, detail="Cannot approve after start time")
    else:
        process_steps = process_step_db.get_process_steps(db, db_car_booking.process_step.process_id)
        current_process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                                       db_car_booking.process_step.process_id,
                                                                                       db_car_booking.process_step.step)
        next_process_step = current_process_step
        is_done = False
        for i in range(len(process_steps)):
            if current_process_step.id == process_steps[i].id:
                if i == len(process_steps) - 1:
                    is_done = True
                else:
                    next_process_step = process_steps[i + 1]
                break
        query = update(models.CarBooking).where(
            and_(models.CarBooking.is_deleted == False, models.CarBooking.id == car_booking_id)
        ).values(
            status=current_process_step.approve_status,
            process_step_id=next_process_step.id,
            is_done=is_done
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.CarBooking).where(models.CarBooking.id == car_booking_id)).first()
        return updated_row


def deny_car_booking(db: Session, car_booking_id: int, user: schemas.User):
    db_car_booking = general_request_db.get_model_by_id(db, car_booking_id, models.CarBooking)
    if db_car_booking.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to deny")
    elif db_car_booking.is_done:
        raise HTTPException(status_code=400, detail="Car booking have already denied or completed")
    else:
        process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                               db_car_booking.process_step.process_id,
                                                                               db_car_booking.process_step.step)
        query = update(models.CarBooking).where(
            and_(models.CarBooking.is_deleted == False, models.CarBooking.id == car_booking_id)
        ).values(
            status=process_step.deny_status,
            is_done=True
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.CarBooking).where(models.CarBooking.id == car_booking_id)).first()
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
