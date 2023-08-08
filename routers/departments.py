#####
##### Room APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from fastapi import APIRouter

from database import department_db
from dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/departments")
async def add_department(department: schemas.DepartmentCreate, user: schemas.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return department_db.add_department(db, department)


@router.get("/departments")
async def get_all_departments(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return department_db.get_all_departments(db)


@router.get("/departments/{id}")
async def get_department_by_id(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return department_db.get_department_by_id(db, id)


# @router.get("/departments/search/")
# async def search_department(key: str, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return department_db.search_department(db, key)


@router.put("/departments/{id}")
async def update_department(id: int, department: schemas.DepartmentCreate,
                            user: schemas.User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    return department_db.update_department(db, id, department)


@router.delete("/departments/{id}")
async def delete_department(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return department_db.delete_department(db, id)
