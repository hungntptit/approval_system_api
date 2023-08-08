import json

import schemas
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session, joinedload

import models


def add_room_booking(db: Session, room_booking: schemas.RoomBookingCreate):
    query = insert(models.RoomBooking).values(
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
    inserted_row = db.scalars(select(models.RoomBooking).where(models.RoomBooking.id == result.lastrowid)).first()
    return inserted_row


def update_room_booking(db: Session, id: int, room_booking: schemas.RoomBookingCreate):
    query = update(models.RoomBooking).where(
        (models.RoomBooking.is_deleted == False) & (models.RoomBooking.id == id)
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


def get_room_booking_by_id(db: Session, room_booking_id: int):
    query = select(models.RoomBooking).where(models.RoomBooking.id == room_booking_id)
    result = db.scalars(query)
    return result.first()


def get_room_bookings_by_user(db: Session, user_id: int):
    query = select(models.RoomBooking).where(models.RoomBooking.user_id == user_id)
    results = db.scalars(query)
    return results.all()


def get_room_bookings_by_role(db: Session, user: schemas.User):
    query = ""
    print(user.role)
    if user.role == "user":
        query = select(models.RoomBooking).where(models.RoomBooking.user_id == user.id)
    elif user.role == "manager":
        query = select(models.RoomBooking).where(
            models.RoomBooking.status.like("%pending%") | models.RoomBooking.status.like("%manager%"))
    elif user.role == "hr":
        query = select(models.RoomBooking).where(
            models.RoomBooking.status.like("%approved by manager%") | models.RoomBooking.status.like("%hr%"))

    results = db.scalars(query)
    return results.all()


def get_room_bookings_by_status(db: Session, status: str):
    query = select(models.RoomBooking).where(models.RoomBooking.status.like(f"%{status}%"))
    result = db.scalars(query)
    return result.all()


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
