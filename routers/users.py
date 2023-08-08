import time
from datetime import timedelta

import jwt
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import schemas
from fastapi import APIRouter, HTTPException

from database import user_db
from dependencies import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, \
    verify_password, SECRET_KEY, ALGORITHM, get_current_user, get_db

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#####
##### User APIs
#####

@router.post("/register")
async def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username has registered")
    db_user = user_db.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email has registered")
    user.password = get_password_hash(user.password)
    inserted_user_id = user_db.register(db=db, user=user)
    return {"inserted_user_id": inserted_user_id}


@router.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_username(db=db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    db_password = db_user.password
    if verify_password(user.password, db_password):
        # correct
        payload = {"id": db_user.id, "sub": user.username, "role": db_user.role,
                   "exp": int((time.time() + 3600) * 1000)}
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        return token
    raise HTTPException(status_code=400, detail="Invalid username or password")

# @router.get("/protected")
# async def protected(user: schemas.User = Depends(get_current_user)):
#     return {"user": user}
