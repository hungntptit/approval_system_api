import json

from sqlalchemy import select, insert, update, and_

import models
import schemas
from sqlalchemy.orm import Session


def add_department(db: Session, department: schemas.DepartmentCreate):
    query = insert(models.Department).values(name=department.name)
    print(query)
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.Department).where(models.Department.id == result.lastrowid)).first()
    return inserted_row


# def search_department(db: Session, key: str):
#     key = f"%{key}%"
#     query = select(models.Department).where(models.Department.name.like(key) & models.Department.is_deleted == False)
#     print(query)
#     return db.scalars(query).all()


def get_department_by_id(db: Session, department_id: int):
    query = select(models.Department).where(
        and_(models.Department.is_deleted == False, models.Department.id == department_id))
    print(query)
    return db.scalars(query).first()


def get_all_departments(db: Session):
    query = select(models.Department).where(models.Department.is_deleted == False)
    return db.scalars(query).all()


def update_department(db: Session, department_id: int, department: schemas.DepartmentCreate):
    query = update(models.Department).where(
        and_(models.Department.is_deleted == False, models.Department.id == department_id)
    ).values(name=department.name)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.Department).where(models.Department.id == department_id)).first()
    return updated_row


def delete_department(db: Session, department_id: int):
    query = update(models.Department).where(
        and_(models.Department.is_deleted == False, models.Department.id == department_id)
    ).values(is_deleted=1)
    result = db.execute(query)
    db.commit()
    deleted_row = db.scalars(select(models.Department).where(models.Department.id == department_id)).first()
    return deleted_row
