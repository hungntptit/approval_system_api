import json

from sqlalchemy import select, insert, update

import models
import schemas
from sqlalchemy.orm import Session


def add_room(db: Session, room: schemas.RoomCreate):
    query = insert(models.Room).values(name=room.name, capacity=room.capacity)
    print(query)
    result = db.execute(query)
    db.commit()
    inserted_row = db.scalars(select(models.Room).where(models.Room.id == result.lastrowid)).first()
    return inserted_row


def search_room(db: Session, key: str):
    key = f"%{key}%"
    query = select(models.Room).where(models.Room.name.like(key) & models.Room.is_deleted == False)
    print(query)
    return db.scalars(query).all()


def get_room_by_id(db: Session, room_id: int):
    query = select(models.Room).where((models.Room.id == room_id) & (models.Room.is_deleted == False))
    print(query)
    return db.scalars(query).first()


def get_all_rooms(db: Session):
    query = select(models.Room).where(models.Room.is_deleted == False)
    return db.scalars(query).all()


def update_room(db: Session, room_id: int, room: schemas.RoomCreate):
    query = update(models.Room).where((models.Room.id == room_id) & (models.Room.is_deleted == False)).values(
        name=room.name,
        capacity=room.capacity)
    result = db.execute(query)
    db.commit()
    updated_row = db.scalars(select(models.Room).where(models.Room.id == room_id)).first()
    return updated_row


def delete_room(db: Session, room_id: int):
    query = update(models.Room).where((models.Room.id == room_id) & (models.Room.is_deleted == False)).values(is_deleted=1)
    result = db.execute(query)
    db.commit()
    deleted_row = db.scalars(select(models.Room).where(models.Room.id == room_id)).first()
    return deleted_row
