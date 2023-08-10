#####
##### Process Steps APIs
#####
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from database import process_step_db
from dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/process_steps")
async def add_process_steps(process_step: schemas.ProcessStepCreate, user: schemas.User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    return process_step_db.add_process_step(db, process_step)


@router.get("/process_steps/")
async def get_process_steps_by_process_id(process_id: int, user: schemas.User = Depends(get_current_user),
                                          db: Session = Depends(get_db)):
    return process_step_db.get_process_steps(db, process_id)


@router.get("/process_steps/{id}")
async def get_process_step_by_id(id: int, user: schemas.User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    return process_step_db.get_process_step_by_id(db, id)


@router.put("/process_steps/{id}")
async def update_process_step(id: int, process_step: schemas.ProcessStepCreate,
                              user: schemas.User = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    return process_step_db.update_process_step(db, id, process_step)


@router.delete("/process_steps/{id}")
async def delete_process_step(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return process_step_db.delete_process_step(db, id)
