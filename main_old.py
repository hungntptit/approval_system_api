# import time
# from datetime import timedelta, datetime
#
# import jose.jwt
# from fastapi import FastAPI, HTTPException
# from fastapi.params import Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from starlette import status
# from starlette.middleware.cors import CORSMiddleware
#
# import models
# import schemas
# from database import user_db, room_db, room_booking_db
# from models import SessionLocal
#
# app = FastAPI()
#
# origins = [
#     "http://localhost:5173",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# SECRET_KEY = "1d400dc44eb021dfa81dbc7c1b4fb51f3b32ae56b6574e19795b045cb4e84ea1"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
#     user = user_db.get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jose.jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#     except jose.JWTError:
#         raise credentials_exception
#     user = user_db.get_user_by_username(db, username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# @app.post("/token", response_model=schemas.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# #####
# ##### User APIs
# #####
#
# @app.post("/register")
# async def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
#     db_user = user_db.get_user_by_username(db=db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="username has registered")
#     db_user = user_db.get_user_by_email(db=db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="email has registered")
#     user.password = get_password_hash(user.password)
#     inserted_user_id = user_db.register(db=db, user=user)
#     return {"inserted_user_id": inserted_user_id}
#
#
# @app.post("/login")
# async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = user_db.get_user_by_username(db=db, username=user.username)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     db_password = db_user.password
#     if verify_password(user.password, db_password):
#         # correct
#         payload = {"id": db_user.id, "sub": user.username, "role": db_user.role,
#                    "exp": int((time.time() + 3600) * 1000)}
#         token = jose.jwt.encode(payload, SECRET_KEY, ALGORITHM)
#         return token
#     raise HTTPException(status_code=400, detail="Invalid username or password")
#
#
# @app.get("/protected")
# async def protected(user: schemas.User = Depends(get_current_user)):
#     return {"user": user}
#
#
# #####
# ##### Room APIs
# #####
#
# @app.post("/room/add")
# async def add_room(room: schemas.RoomCreate, user: schemas.User = Depends(get_current_user),
#                    db: Session = Depends(get_db)):
#     return room_db.add_room(db, room)
#
#
# @app.get("/room/all")
# async def get_all_rooms(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return room_db.get_all_rooms(db)
#
#
# @app.get("/room/{id}")
# async def get_room_by_id(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return room_db.get_room_by_id(db, id)
#
#
# # @app.get("/room/search/")
# # async def search_room(key: str, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
# #     return room_db.search_room(db, key)
#
#
# @app.put("/room/{id}")
# async def update_room(id: int, room: schemas.RoomCreate, user: schemas.User = Depends(get_current_user),
#                       db: Session = Depends(get_db)):
#     return room_db.update_room(db, id, room)
#
#
# @app.delete("/room/{id}")
# async def delete_room(id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return room_db.delete_room(db, id)
#
#
# #####
# ##### Request APIs
# #####
# @app.get("/room_booking/user")
# async def get_requests_by_user(user: schemas.User = Depends(get_current_user),
#                                db: Session = Depends(get_db)):
#     results = room_booking_db.get_requests_by_user(db, user.id)
#     return results
#
#
# @app.get("/room_booking/role")
# async def get_requests_by_role(user: schemas.User = Depends(get_current_user),
#                                db: Session = Depends(get_db)):
#     results = room_booking_db.get_requests_by_role(db, user)
#     return results
#
#
# # @app.get("/room_booking/pending")
# # async def get_pending_request(user: schemas.User = Depends(get_current_user),
# #                               db: Session = Depends(get_db)):
# #     if user.role == "manager":
# #         return room_booking_db.get_requests_by_status(db, "pending")
# #     elif user.role == "hr":
# #         return room_booking_db.get_requests_by_status(db, "approved by manager")
# #
# #
# # @app.get("/room_booking/processed")
# # async def get_processed_request(user: schemas.User = Depends(get_current_user),
# #                                 db: Session = Depends(get_db)):
# #     if user.role == "manager":
# #         return room_booking_db.get_requests_by_status(db, "manager")
# #     elif user.role == "hr":
# #         return room_booking_db.get_requests_by_status(db, "hr")
#
#
# @app.post("/room_booking/add")
# async def add_request(request: schemas.RequestCreate, user: schemas.User = Depends(get_current_user),
#                       db: Session = Depends(get_db)):
#     room: models.Room = room_db.get_room_by_id(db, request.room_id)
#     if room.capacity < request.participation:
#         raise HTTPException(status_code=400, detail="Room does not have enough capacity.")
#     if room_booking_db.check_available_room(db, request):
#         return room_booking_db.add_request(db, request)
#     else:
#         raise HTTPException(status_code=400, detail="Room is not available.")
#
#
# @app.put("/room_booking/approve")
# async def approve_request(request_id: int, user: schemas.User = Depends(get_current_user),
#                           db: Session = Depends(get_db)):
#     db_request = room_booking_db.get_requests_by_id(db, request_id)
#     if user.role == "manager" and db_request.status == "pending":
#         if room_booking_db.check_available_room(db, db_request):
#             return room_booking_db.approve_request(db, request_id, user.role)
#         else:
#             raise HTTPException(status_code=400, detail="Room is not available.")
#     elif user.role == "hr" and db_request.status == "approved by manager":
#         return room_booking_db.approve_request(db, request_id, user.role)
#     else:
#         raise HTTPException(status_code=400, detail="Cannot approve.")
#
#
# @app.put("/room_booking/deny")
# async def deny_request(request_id: int, user: schemas.User = Depends(get_current_user),
#                        db: Session = Depends(get_db)):
#     return room_booking_db.deny_request(db, request_id, user.role)
