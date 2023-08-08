from datetime import datetime, date, time

import timestamp as timestamp
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    password: str


class UserRegister(UserBase):
    name: str
    email: str


class UserLogin(UserBase):
    pass


class User(UserRegister):
    id: int
    role: str
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    name: str
    capacity: int


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True


class RoomBookingBase(BaseModel):
    user_id: int
    room_id: int
    title: str
    place: str
    participation: int
    booking_date: date
    start_time: time
    end_time: time


class RoomBookingCreate(RoomBookingBase):
    pass


class RoomBooking(RoomBookingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    is_deleted: bool

    class Config:
        from_attributes = True


class CarBase(BaseModel):
    name: str
    seats: int


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True


class CarBookingBase(BaseModel):
    user_id: int
    car_id: int
    title: str
    place: str
    start_time: datetime
    end_time: datetime
    origin: str
    destination: str
    distance: float
    number_of_people: int


class CarBookingCreate(CarBookingBase):
    pass


class CarBooking(CarBookingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    is_deleted: bool

    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True


class BuyingRequestBase(BaseModel):
    user_id: int
    department_id: int
    title: str
    description: str
    approve_before: datetime
    place: str


class BuyingRequestCreate(BuyingRequestBase):
    pass


class BuyingRequest(BuyingRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    is_deleted: bool

    class Config:
        from_attributes = True
