#####
##### Room APIs
#####
from fastapi.params import Depends
from sqlalchemy.orm import Session

import schemas
from fastapi import APIRouter

from database import room_db
from dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/rooms")
async def add_room(room: schemas.RoomCreate, user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return room_db.add_room(db, room)


@router.get("/rooms")
async def get_all_rooms(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_db.get_all_rooms(db)


@router.get("/rooms/{id}")
async def get_room_by_id(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_db.get_room_by_id(db, id)


# @router.get("/rooms/search/")
# async def search_room(key: str, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return room_db.search_room(db, key)


@router.put("/rooms/{id}")
async def update_room(id: int, room: schemas.RoomCreate, user: schemas.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return room_db.update_room(db, id, room)


@router.delete("/rooms/{id}")
async def delete_room(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_db.delete_room(db, id)

