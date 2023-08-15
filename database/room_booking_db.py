import json

import schemas
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session, joinedload

import models
from database import process_step_db


def add_room_booking(db: Session, room_booking: schemas.RoomBookingCreate):
    process_step = process_step_db.get_process_step_by_process_id_and_step(db, 1, 1)
    print(process_step)
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
            is_deleted=room_booking.is_deleted,

            room=room_booking.room,
            process_step=room_booking.process_step
        )
        ls.append(rb)
    return ls


def approve_room_booking(db: Session, room_booking_id: int, role: str):
    query = update(models.RoomBooking).where(models.RoomBooking.id == room_booking_id).values(
        status="approved by " + role)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)).first()
    return updated_row


def deny_room_booking(db: Session, room_booking_id: int, role: str):
    query = update(models.RoomBooking).where(models.RoomBooking.id == room_booking_id).values(
        status="denied by " + role)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)).first()
    return updated_row


def get_room_booking_by_id(db: Session, room_booking_id: int):
    query = select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)
    result = db.scalars(query)
    ls = convert_result_to_room_booking(result)
    if len(ls) > 0:
        return ls[0]
    return None


def get_room_bookings_by_role(db: Session, user: schemas.User):
    process_steps = process_step_db.get_process_steps(db, 1, user.role)
    process_steps_int = [i.step for i in process_steps]
    # print(process_steps_int)
    next_process_steps_int = [i.step + 1 for i in process_steps]
    query = select(models.RoomBooking).join(models.ProcessStep).where(
        and_(
            models.RoomBooking.is_deleted == False,
            or_(models.ProcessStep.step.in_(process_steps_int),
                models.ProcessStep.step.in_(next_process_steps_int)
                )
        )
    ).order_by(models.ProcessStep.step.asc(), models.BuyingRequest.is_done.asc(),
               models.BuyingRequest.approve_before.asc())
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_room_booking(result)


def get_room_bookings_by_user(db: Session, user: schemas.User):
    query = select(models.RoomBooking).join(models.ProcessStep).where(
        and_(models.RoomBooking.is_deleted == False, models.RoomBooking.user_id == user.id)
    ).order_by(models.ProcessStep.step.asc(), models.RoomBooking.is_done.asc(),
               models.RoomBooking.approve_before.asc())
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_room_booking(result)


def check_available_room(db: Session, room_booking: schemas.RoomBookingCreate):
    room_id = room_booking.room_id
    booking_date = room_booking.booking_date
    start_time = room_booking.start_time
    end_time = room_booking.end_time
    participation = room_booking.participation
    query = select(models.RoomBooking).where(
        (models.RoomBooking.room_id == room_id) &
        (models.RoomBooking.is_deleted == False) &
        (models.RoomBooking.status.like("%approved%")) &
        (models.RoomBooking.booking_date == booking_date) &
        (
            (models.RoomBooking.start_time.between(start_time, end_time) |
             (models.RoomBooking.end_time.between(start_time, end_time) |
              (
                      (models.RoomBooking.start_time <= start_time) &
                      (models.RoomBooking.end_time >= end_time))
              ))
        )
    )
    print(query)
    result = db.execute(query)
    for row in result:
        print(row)
    print(result.all())
    return result.first() == None
