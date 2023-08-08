import json

from sqlalchemy import select, insert, update

import models
import schemas
from sqlalchemy.orm import Session


def add_car(db: Session, car: schemas.CarCreate):
    query = insert(models.Car).values(name=car.name, seats=car.seats)
    print(query)
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.Car).where(models.Car.id == result.lastrowid)).first()
    return inserted_row


# def search_car(db: Session, key: str):
#     key = f"%{key}%"
#     query = select(models.Car).where(models.Car.name.like(key) & models.Car.is_deleted == False)
#     print(query)
#     return db.scalars(query).all()


def get_car_by_id(db: Session, car_id: int):
    query = select(models.Car).where((models.Car.is_deleted == False) & (models.Car.id == car_id))
    print(query)
    return db.scalars(query).first()


def get_all_cars(db: Session):
    query = select(models.Car).where(models.Car.is_deleted == False)
    return db.scalars(query).all()


def update_car(db: Session, car_id: int, car: schemas.CarCreate):
    query = update(models.Car).where((models.Car.is_deleted == False) & (models.Car.id == car_id)).values(
        name=car.name,
        seats=car.seats
    )
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.Car).where(models.Car.id == car_id)).first()
    return updated_row


def delete_car(db: Session, car_id: int):
    query = update(models.Car).where((models.Car.is_deleted == False) & (models.Car.id == car_id)).values(is_deleted=1)
    result = db.execute(query)
    db.commit()
    deleted_row = db.scalars(select(models.Car).where(models.Car.id == car_id)).first()
    return deleted_row
