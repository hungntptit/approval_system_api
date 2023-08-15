#####
##### Processes APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from fastapi import APIRouter

from database import room_db, process_db
from dependencies import get_db, get_current_user

router = APIRouter()


@router.get("/processes")
async def get_all_processes(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return process_db.get_all_processes(db)
