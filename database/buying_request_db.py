import datetime

from fastapi import HTTPException
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session

import models
import schemas
from database import process_step_db

import sys

sys.stdout.reconfigure(encoding="utf-8")


def add_buying_request(db: Session, buying_request: schemas.BuyingRequestCreate):
    process_step = process_step_db.get_process_step_by_process_id_and_step(db, 3, 1)
    print(process_step)
    query = insert(models.BuyingRequest).values(
        user_id=buying_request.user_id,
        department_id=buying_request.department_id,
        process_step_id=process_step.id,
        title=buying_request.title,
        description=buying_request.description,
        approve_before=buying_request.approve_before,
        place=buying_request.place
    )
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.BuyingRequest).where(models.BuyingRequest.id == result.lastrowid)).first()
    return inserted_row


def update_buying_request(db: Session, id: int, buying_request: schemas.BuyingRequestCreate):
    query = update(models.BuyingRequest).where(
        and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.id == id)
    ).values(
        user_id=buying_request.user_id,
        department_id=buying_request.department_id,
        title=buying_request.title,
        description=buying_request.description,
        approve_before=buying_request.approve_before,
        place=buying_request.place
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.BuyingRequest).where((models.BuyingRequest.id == id))).first()
    return updated_row


def approve_buying_request(db: Session, buying_request_id: int, user: models.User):
    db_buying_request = get_buying_request_by_id(db, buying_request_id)
    # print(db_buying_request.approve_before)
    # print(datetime.datetime.now())
    if db_buying_request.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authenticated to approve")
    elif db_buying_request.is_done:
        raise HTTPException(status_code=400, detail="Buying request have already denied or completed")
    elif db_buying_request.approve_before < datetime.datetime.now():
        raise HTTPException(status_code=400, detail="Cannot approve after approve date")
    else:
        # print(db_buying_request.process_step.process_id)
        process_steps = process_step_db.get_process_steps(db, db_buying_request.process_step.process_id)
        print(process_steps)
        current_process_step = process_step_db.get_process_step_by_process_id_and_step(db, db_buying_request.process_step.process_id,
                                                                                       db_buying_request.process_step.step)
        next_process_step = current_process_step
        print(next_process_step.step)
        is_done = False
        for i in range(len(process_steps)):
            print(current_process_step, process_steps[i])
            print(current_process_step.id == process_steps[i].id)
            if current_process_step.id == process_steps[i].id:
                if i == len(process_steps) - 1:
                    is_done = True
                else:
                    next_process_step = process_steps[i + 1]
                break
        print(next_process_step.step)
        query = update(models.BuyingRequest).where(
            and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.id == buying_request_id)
        ).values(
            status=current_process_step.approve_status,
            process_step_id=next_process_step.id,
            is_done=is_done
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.BuyingRequest).where(models.BuyingRequest.id == buying_request_id)).first()
        return updated_row


def deny_buying_request(db: Session, buying_request_id: int, user: models.User):
    db_buying_request = get_buying_request_by_id(db, buying_request_id)
    if db_buying_request.process_step.role != user.role:
        raise HTTPException(status_code=401, detail="Not authenticated to deny")
    elif db_buying_request.is_done:
        raise HTTPException(status_code=400, detail="Buying request have already denied or completed")
    else:
        process_step = process_step_db.get_process_step_by_process_id_and_step(db, db_buying_request.process_step.process_id,
                                                                               db_buying_request.process_step.step)
        query = update(models.BuyingRequest).where(
            and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.id == buying_request_id)
        ).values(
            status=process_step.deny_status,
            is_done=True
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.BuyingRequest).where(models.BuyingRequest.id == buying_request_id)).first()
        return updated_row


def set_buying_request_status(db: Session, buying_request_id: int, status: str):
    query = update(models.BuyingRequest).where(
        and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.id == buying_request_id)
    ).values(
        status=status)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.BuyingRequest).where(models.BuyingRequest.id == buying_request_id)).first()
    return updated_row


def convert_result_to_buying_request(result):
    list = []
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
        list.append(br)
    return list


def get_buying_request_by_id(db: Session, buying_request_id: int):
    query = select(models.BuyingRequest).join(models.ProcessStep).where(
        and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.id == buying_request_id)
    )
    # print(query)
    result = db.scalars(query).all()
    list = convert_result_to_buying_request(result)
    if len(list) > 0:
        return list[0]
    return None


def get_buying_requests_by_role(db: Session, user: schemas.User):
    process_steps = process_step_db.get_process_steps(db, 3, user.role)
    process_steps_int = [i.step for i in process_steps]
    # print(process_steps_int)
    next_process_steps_int = [i.step + 1 for i in process_steps]
    query = select(models.BuyingRequest).join(models.ProcessStep).where(
        and_(
            models.BuyingRequest.is_deleted == False,
            or_(models.ProcessStep.step.in_(process_steps_int),
                models.ProcessStep.step.in_(next_process_steps_int)
                )
        )
    ).order_by(models.ProcessStep.step.asc(), models.BuyingRequest.is_done.asc(),
               models.BuyingRequest.approve_before.asc())
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_buying_request(result)


def get_buying_requests_by_user(db: Session, user: schemas.User):
    query = select(models.BuyingRequest).join(models.ProcessStep).where(
        and_(models.BuyingRequest.is_deleted == False, models.BuyingRequest.user_id == user.id)
    ).order_by(models.ProcessStep.step.asc(), models.BuyingRequest.is_done.asc(),
               models.BuyingRequest.approve_before.asc())
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_buying_request(result)
