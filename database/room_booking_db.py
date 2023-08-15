import json
import time
import datetime

from fastapi import HTTPException

import schemas
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session, joinedload

import models
from database import process_step_db


def add_room_booking(db: Session, room_booking: schemas.RoomBookingCreate):
    process_step = process_step_db.get_process_step_by_process_id_and_step(db, 1, 1)
    query = insert(models.RoomBooking).values(
        user_id=room_booking.user_id,
        room_id=room_booking.room_id,
        process_step_id=process_step.id,
        title=room_booking.title,
        place=room_booking.place,
        participation=room_booking.participation,
        booking_date=room_booking.booking_date,
        start_time=room_booking.start_time,
        end_time=room_booking.end_time
    )
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.RoomBooking).where(models.RoomBooking.id == result.lastrowid)).first()
    return inserted_row


def update_room_booking(db: Session, id: int, room_booking: schemas.RoomBookingCreate):
    query = update(models.RoomBooking).where(
        and_(models.RoomBooking.is_deleted == False, models.RoomBooking.id == id)
    ).values(
        user_id=room_booking.user_id,
        room_id=room_booking.room_id,
        title=room_booking.title,
        place=room_booking.place,
        participation=room_booking.participation,
        booking_date=room_booking.booking_date,
        start_time=room_booking.start_time,
        end_time=room_booking.end_time
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.RoomBooking).where(models.RoomBooking.id == result.lastrowid)).first()
    return updated_row


def convert_result_to_room_booking(result):
    ls = []
    for room_booking in result:
        rb = models.RoomBooking(
            id=room_booking.id,
            user_id=room_booking.user_id,
            room_id=room_booking.room_id,
            process_step_id=room_booking.process_step_id,
            title=room_booking.title,
            place=room_booking.place,
            participation=room_booking.participation,
            booking_date=room_booking.booking_date,
            start_time=room_booking.start_time,
            end_time=room_booking.end_time,
            created_at=room_booking.created_at,
            updated_at=room_booking.updated_at,
            status=room_booking.status,
            is_done=room_booking.is_done,
            is_deleted=room_booking.is_deleted,

            room=room_booking.room,
            process_step=room_booking.process_step
        )
        ls.append(rb)
    return ls


def approve_room_booking(db: Session, room_booking_id: int, user: schemas.User):
    db_room_booking = get_room_booking_by_id(db, room_booking_id)
    if db_room_booking.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to approve")
    elif db_room_booking.is_done:
        raise HTTPException(status_code=400, detail="Room booking have already denied or completed")
    elif (db_room_booking.booking_date == datetime.date.today() and
          db_room_booking.start_time < datetime.datetime.now().time()) or \
            db_room_booking.booking_date < datetime.date.today():
        raise HTTPException(status_code=400, detail="Cannot approve after booking date")
    else:
        process_steps = process_step_db.get_process_steps(db, db_room_booking.process_step.process_id)
        current_process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                                       db_room_booking.process_step.process_id,
                                                                                       db_room_booking.process_step.step)
        next_process_step = current_process_step
        is_done = False
        for i in range(len(process_steps)):
            if current_process_step.id == process_steps[i].id:
                if i == len(process_steps) - 1:
                    is_done = True
                else:
                    next_process_step = process_steps[i + 1]
                break
        query = update(models.RoomBooking).where(
            and_(models.RoomBooking.is_deleted == False, models.RoomBooking.id == room_booking_id)
        ).values(
            status=current_process_step.approve_status,
            process_step_id=next_process_step.id,
            is_done=is_done
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)).first()
        return updated_row


def deny_room_booking(db: Session, room_booking_id: int, user: schemas.User):
    db_room_booking = get_room_booking_by_id(db, room_booking_id)
    if db_room_booking.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to deny")
    elif db_room_booking.is_done:
        raise HTTPException(status_code=400, detail="Room booking have already denied or completed")
    else:
        process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                               db_room_booking.process_step.process_id,
                                                                               db_room_booking.process_step.step)
        query = update(models.RoomBooking).where(
            and_(models.RoomBooking.is_deleted == False, models.RoomBooking.id == room_booking_id)
        ).values(
            status=process_step.deny_status,
            is_done=True
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)).first()
        return updated_row


def check_available_room(db: Session, room_booking: schemas.RoomBookingCreate):
    room_id = room_booking.room_id
    booking_date = room_booking.booking_date
    start_time = room_booking.start_time
    end_time = room_booking.end_time
    participation = room_booking.participation
    query = select(models.RoomBooking).where(
        and_(
            models.RoomBooking.room_id == room_id,
            models.RoomBooking.is_deleted == False,
            models.RoomBooking.process_step.step > 1,
            models.RoomBooking.booking_date == booking_date,
            or_(
                models.RoomBooking.start_time.between(start_time, end_time),
                models.RoomBooking.end_time.between(start_time, end_time),
                and_(models.RoomBooking.start_time <= start_time, models.RoomBooking.end_time >= end_time)
            )
        ))
    result = db.execute(query)
    return result.first() == None
