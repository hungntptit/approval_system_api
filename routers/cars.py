#####
##### Room APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from fastapi import APIRouter

from database import car_db
from dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/cars")
async def add_car(car: schemas.CarCreate, user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    return car_db.add_car(db, car)


@router.get("/cars")
async def get_all_cars(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return car_db.get_all_cars(db)


@router.get("/cars/{id}")
async def get_car_by_id(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return car_db.get_car_by_id(db, id)


# @router.get("/cars/search/")
# async def search_car(key: str, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return car_db.search_car(db, key)


@router.put("/cars/{id}")
async def update_car(id: int, car: schemas.CarCreate, user: schemas.User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    return car_db.update_car(db, id, car)


@router.delete("/cars/{id}")
async def delete_car(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return car_db.delete_car(db, id)
