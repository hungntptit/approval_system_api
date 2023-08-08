from sqlalchemy import select, insert

import schemas
from sqlalchemy.orm import Session

import models


def get_user(db: Session, user_id: int):
    query = select(models.User).where(models.User.id == user_id)
    result = db.scalars(query)
    return result.first()


def get_user_by_username(db: Session, username: str):
    query = select(models.User).where(models.User.username == username)
    result = db.scalars(query)
    return result.first()


def get_user_by_email(db: Session, email: str):
    query = select(models.User).where((models.User.email == email) & (models.User.is_deleted == False))
    result = db.scalars(query)
    return result.first()


def get_users(db: Session):
    query = select(models.User).where(models.User.is_deleted == False)
    result = db.scalars(query)
    return result.all()


def register(db: Session, user: schemas.UserRegister):
    query = insert(models.User).values(username=user.username, email=user.email, password=user.password, name=user.name)
    print(query)
    result = db.execute(query)
    db.commit()
    return result.lastrowid
