from sqlalchemy import select
from sqlalchemy.orm import Session

import models


def convert_result_to_process_step(result):
    ls = []
    for process_step in result:
        ps = models.ProcessStep(
            process_id=process_step.process_id,
            step=process_step.step,
            name=process_step.name,
            role=process_step.role,
            approve_status=process_step.approve_status,
            deny_status=process_step.deny_status
        )
        ls.append(ps)
    return ls


def get_process_steps(db: Session, process_id: int, role: str = None):
    query = select(models.ProcessStep).where(
        (models.ProcessStep.process_id == process_id)
    )
    if role:
        query = select(models.ProcessStep).where(
            (models.ProcessStep.process_id == process_id) & (models.ProcessStep.role == role)
        )
    result = db.scalars(query).all()
    return convert_result_to_process_step(result)


def get_process_step(db: Session, process_id: int, process_step: int):
    query = select(models.ProcessStep).where(
        (models.ProcessStep.process_id == process_id) & (models.ProcessStep.step == process_step)
    )
    result = db.scalars(query).all()
    ls = convert_result_to_process_step(result)
    if len(ls) > 0:
        return ls[0]
    return None
