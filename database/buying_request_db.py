import datetime

from fastapi import HTTPException
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.orm import Session

import models
import schemas
from database import process_step_db, general_request_db

import sys

sys.stdout.reconfigure(encoding="utf-8")


def add_buying_request(db: Session, buying_request: schemas.BuyingRequestCreate):
    process_step = process_step_db.get_process_step_by_process_id_and_step(db, 3, 1)
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
