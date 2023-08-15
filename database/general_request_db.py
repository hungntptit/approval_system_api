import datetime

from fastapi import HTTPException
from sqlalchemy import select, and_, or_, update
from sqlalchemy.orm import Session

import models
import schemas
from database import process_step_db


def convert_result_to_model(result, model):
    ls = []
    if model == models.RoomBooking:
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
    elif model == models.CarBooking:
        for car_booking in result:
            cb = models.CarBooking(
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
            ls.append(cb)
    elif model == models.BuyingRequest:
        for buying_request in result:
            br = models.BuyingRequest(
                id=buying_request.id,
                user_id=buying_request.user_id,
                department_id=buying_request.department_id,
                process_step_id=buying_request.process_step_id,
                title=buying_request.title,
                description=buying_request.description,
                approve_before=buying_request.approve_before,
                place=buying_request.place,
                created_at=buying_request.created_at,
                updated_at=buying_request.updated_at,
                status=buying_request.status,
                is_done=buying_request.is_done,
                is_deleted=buying_request.is_deleted,

                department=buying_request.department,
                process_step=buying_request.process_step
            )
            ls.append(br)
    return ls


def get_model_by_id(db: Session, id: int, model):
    query = select(model).where(
        and_(model.is_deleted == False, model.id == id))
    result = db.scalars(query)
    ls = convert_result_to_model(result, model)
    if len(ls) > 0:
        return ls[0]
    return None


def get_model_by_role(db: Session, user: schemas.User, model):
    process_steps = process_step_db.get_process_steps(db, 1, user.role)
    process_steps_int = [i.step for i in process_steps]
    next_process_steps_int = [i.step + 1 for i in process_steps]
    query = select(model).join(models.ProcessStep).where(
        and_(
            model.is_deleted == False,
            or_(models.ProcessStep.step.in_(process_steps_int),
                models.ProcessStep.step.in_(next_process_steps_int)
                )
        )
    ).order_by(models.ProcessStep.step.asc(), model.is_done.asc())
    result = db.scalars(query).all()
    return convert_result_to_model(result, model)


def get_model_by_user(db: Session, user: schemas.User, model):
    query = select(model).join(models.ProcessStep).where(
        and_(model.is_deleted == False, model.user_id == user.id)
    ).order_by(models.ProcessStep.step.asc(), model.is_done.asc())
    result = db.scalars(query).all()
    return convert_result_to_model(result, model)


def approve_model(db: Session, model_id: int, user: schemas.User, model):
    db_model = get_model_by_id(db, model_id)
    if db_model.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to approve")
    elif db_model.is_done:
        raise HTTPException(status_code=400, detail="Request have already denied or completed")

    if model == models.RoomBooking:
        if (db_model.booking_date == datetime.date.today() and db_model.start_time < datetime.datetime.now().time()) or \
                db_model.booking_date < datetime.date.today():
            raise HTTPException(status_code=400, detail="Cannot approve after booking date")
    elif model == models.CarBooking:
        if db_model.start_time < datetime.datetime.now().time():
            raise HTTPException(status_code=400, detail="Cannot approve after start time")
    elif model == models.BuyingRequest:
        if db_model.approve_before < datetime.datetime.now():
            raise HTTPException(status_code=400, detail="Cannot approve after approve date")

    process_steps = process_step_db.get_process_steps(db, db_model.process_step.process_id)
    current_process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                                   db_model.process_step.process_id,
                                                                                   db_model.process_step.step)
    next_process_step = current_process_step
    is_done = False
    for i in range(len(process_steps)):
        if current_process_step.id == process_steps[i].id:
            if i == len(process_steps) - 1:
                is_done = True
            else:
                next_process_step = process_steps[i + 1]
            break
    query = update(model).where(
        and_(model.is_deleted == False, model.id == model_id)
    ).values(
        status=current_process_step.approve_status,
        process_step_id=next_process_step.id,
        is_done=is_done
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(model).where(model.id == model_id)).first()
    return updated_row


def deny_model(db: Session, model_id: int, user: schemas.User, model):
    db_model = get_model_by_id(db, model_id, model)
    if db_model.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authorized to deny")
    elif db_model.is_done:
        raise HTTPException(status_code=400, detail="Request have already denied or completed")
    process_step = process_step_db.get_process_step_by_process_id_and_step(db,
                                                                           db_model.process_step.process_id,
                                                                           db_model.process_step.step)
    query = update(models.CarBooking).where(
        and_(models.CarBooking.is_deleted == False, models.CarBooking.id == model_id)
    ).values(
        status=process_step.deny_status,
        is_done=True
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.CarBooking).where(models.CarBooking.id == model_id)).first()
    return updated_row
