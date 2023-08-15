from fastapi import HTTPException
from sqlalchemy import select, and_, update, delete, insert
from sqlalchemy.orm import Session

import models
import schemas


def convert_result_to_process_step(result):
    ls = []
    for process_step in result:
        ps = models.ProcessStep(
            id=process_step.id,
            process_id=process_step.process_id,
            step=process_step.step,
            name=process_step.name,
            role=process_step.role,
            approve_status=process_step.approve_status,
            deny_status=process_step.deny_status,
            process=process_step.process
        )
        ls.append(ps)
    return ls


def get_process_steps(db: Session, process_id: int, role: str = None):
    query = select(models.ProcessStep).where(models.ProcessStep.process_id == process_id).order_by(
        models.ProcessStep.step)
    if role:
        query = select(models.ProcessStep).where(
            and_(models.ProcessStep.process_id == process_id, models.ProcessStep.role == role,
                 models.ProcessStep.is_deleted == False)
        ).order_by(models.ProcessStep.step)
    result = db.scalars(query).all()
    return convert_result_to_process_step(result)


def get_process_step_by_process_id_and_step(db: Session, process_id: int, step: int):
    query = select(models.ProcessStep).where(
        and_(models.ProcessStep.process_id == process_id, models.ProcessStep.step == step,
             models.ProcessStep.is_deleted == False)
    )
    result = db.scalars(query).all()
    ls = convert_result_to_process_step(result)
    if len(ls) > 0:
        return ls[0]
    return None


def get_process_step_by_id(db: Session, process_step_id: int):
    query = select(models.ProcessStep).where(
        models.ProcessStep.id == process_step_id, models.ProcessStep.is_deleted == False
    )
    result = db.scalars(query).all()
    ls = convert_result_to_process_step(result)
    if len(ls) > 0:
        return ls[0]
    return None


def add_process_step(db: Session, process_step: schemas.ProcessStepCreate):
    process_id = process_step.process_id
    process_steps = get_process_steps(db, process_id)
    step = process_step.step
    max_step = 0
    if len(process_steps) > 0:
        max_step = process_steps[-1].step
    if step > max_step + 1:
        raise HTTPException(status_code=400, detail="Invalid step number " + f"(1 - {max_step + 1}).")
    for i in reversed(range(step, max_step + 1)):
        query1 = update(models.ProcessStep).where(
            and_(models.ProcessStep.process_id == process_id, models.ProcessStep.step == i)
        ).values(
            step=models.ProcessStep.step + 1
        )
        db.execute(query1)

    query = insert(models.ProcessStep).values(
        process_id=process_step.process_id,
        step=process_step.step,
        name=process_step.name,
        role=process_step.role,
        approve_status=process_step.approve_status,
        deny_status=process_step.deny_status
    )
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.ProcessStep).where(models.ProcessStep.id == result.lastrowid)).first()
    return inserted_row


def update_process_step(db: Session, process_step_id: int, process_step: schemas.ProcessStepCreate):
    query = update(models.ProcessStep).where(
        and_(models.ProcessStep.id == process_step_id, models.ProcessStep.is_deleted == False)
    ).values(
        name=process_step.name,
        role=process_step.role,
        approve_status=process_step.approve_status,
        deny_status=process_step.deny_status
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.ProcessStep).where(models.ProcessStep.id == process_step_id)).first()
    return updated_row


def delete_process_step(db: Session, process_step_id: int):
    db_process_step = get_process_step_by_id(db, process_step_id)
    if not db_process_step:
        raise HTTPException(status_code=400, detail="Cannot delete process step.")
    process_steps = get_process_steps(db, db_process_step.process_id)

    process_id = db_process_step.process_id
    step = db_process_step.step

    query = delete(models.ProcessStep).where(models.ProcessStep.id == process_step_id)
    try:
        db.execute(query)
        query1 = update(models.ProcessStep).where(
            and_(models.ProcessStep.process_id == process_id, models.ProcessStep.step > step)
        ).values(
            step=models.ProcessStep.step - 1
        )
        db.execute(query1)
    except:
        raise HTTPException(status_code=400, detail="Cannot delete process step.")
    db.commit()
    return {"message": "Process step deleted successfully"}
