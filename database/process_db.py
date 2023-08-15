from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import process_step_db


def convert_result_to_process(db, result):
    ls = []
    for process in result:
        print(process.process_steps)
        pr = models.Process(
            id=process.id,
            name=process.name,
            is_deleted=process.is_deleted,
            # process_steps=process_step_db.get_process_steps(db, process.id)
            process_steps=process.process_steps
        )
        ls.append(pr)
    return ls


def get_all_processes(db: Session):
    return models.Process.query.all()
    # query = select(models.Process).order_by(models.Process.id)
    # result = db.scalars(query).all()
    # return convert_result_to_process(db, result)
