import json

import schemas
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session, joinedload

import models
from database import process_step_db


def add_buying_request(db: Session, buying_request: schemas.BuyingRequestCreate):
    query = insert(models.BuyingRequest).values(
        user_id=buying_request.user_id,
        department_id=buying_request.department_id,
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
        (models.BuyingRequest.is_deleted == False) & (models.BuyingRequest.id == id)
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
    updated_row = db.scalars(select(models.BuyingRequest).where(models.BuyingRequest.id == id)).first()
    return updated_row


def approve_buying_request(db: Session, buying_request_id: int, role: str):
    db_buying_request = get_buying_request_by_id(buying_request_id)
    print(db_buying_request.values())
    query = update(models.BuyingRequest).where(
        (models.BuyingRequest.is_deleted == False)
        & (models.BuyingRequest.id == buying_request_id)
    ).values(
        status="approved by " + role)
    # result = db.execute(query)
    # db.commit()
    updated_row = db.scalars(select(models.BuyingRequest).where(models.BuyingRequest.id == buying_request_id)).first()
    return updated_row


def deny_buying_request(db: Session, buying_request_id: int, user: models.User):
    db_buying_request = get_buying_request_by_id(buying_request_id)
    if db_buying_request.process_step.role == user.role:
        process_step = process_step_db.get_process_steps_by_process_id(db, db_buying_request.process_id,
                                                                       db_buying_request.process_step)
        query = update(models.BuyingRequest).where(
            (models.BuyingRequest.is_deleted == False)
            & (models.BuyingRequest.id == buying_request_id)
        ).values(
            status=process_step.deny_status,
            is_done=True
        )
        result = db.execute(query)
        db.commit()
        updated_row = db.scalars(
            select(models.BuyingRequest).where(models.BuyingRequest.id == buying_request_id)).first()
        return updated_row
    return None


def set_buying_request_status(db: Session, buying_request_id: int, status: str):
    query = update(models.BuyingRequest).where(
        (models.BuyingRequest.is_deleted == False)
        & (models.BuyingRequest.id == buying_request_id)
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
            process_id=buying_request.process_id,
            process_step=buying_request.process_step,
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
            step=buying_request.step
        )
        list.append(br)
    return list


def get_buying_request_by_id(db: Session, buying_request_id: int):
    query = select(models.BuyingRequest).join(models.ProcessStep,
                                              (models.BuyingRequest.process_id == models.ProcessStep.process_id)
                                              & (models.BuyingRequest.process_step == models.ProcessStep.step)) \
        .where((models.BuyingRequest.is_deleted == False) & (models.BuyingRequest.id == buying_request_id))
    # print(query)
    result = db.scalars(query).all()
    list = convert_result_to_buying_request(result)
    if len(list) > 0:
        return list[0]
    return None


def get_buying_requests_by_role(db: Session, user: schemas.User):
    query = select(models.BuyingRequest).join(models.ProcessStep,
                                              (models.BuyingRequest.process_id == models.ProcessStep.process_id)
                                              & (models.BuyingRequest.process_step == models.ProcessStep.step)) \
        .where((models.BuyingRequest.is_deleted == False) & (models.ProcessStep.role == user.role))
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_buying_request(result)


def get_buying_requests_by_user(db: Session, user: schemas.User):
    query = select(models.BuyingRequest).join(models.ProcessStep,
                                              (models.BuyingRequest.process_id == models.ProcessStep.process_id)
                                              & (models.BuyingRequest.process_step == models.ProcessStep.step)) \
        .where((models.BuyingRequest.is_deleted == False) & (models.BuyingRequest.user_id == user.id))
    # print(query)
    result = db.scalars(query).all()
    return convert_result_to_buying_request(result)
