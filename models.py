import datetime

from sqlalchemy import Column, Integer, String, Date, Time, TIMESTAMP, ForeignKey, Boolean, CheckConstraint, DateTime, \
    Float, ForeignKeyConstraint

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import models

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:root@localhost:3306/jwtdb"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(length=255), unique=True, index=True)
    email = Column(String(length=255), unique=True, index=True)
    password = Column(String(length=255))
    name = Column(String(length=255))
    role = Column(String(length=255), default='user')
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    is_deleted = Column(Boolean, default=False)

    # room_bookings = relationship("RoomBooking", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255))
    capacity = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    room_bookings = relationship("RoomBooking", back_populates="room")


class RoomBooking(Base):
    __tablename__ = "room_bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    title = Column(String(length=255))
    place = Column(String(length=255))
    participation = Column(Integer)
    booking_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow())
    status = Column(String(length=255), default="pending")
    is_deleted = Column(Boolean, default=False)
    CheckConstraint("start_time < end_time", name="time_constraint")

    room = relationship("Room", back_populates="room_bookings")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255))
    seats = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    car_bookings = relationship("CarBooking", back_populates="car")


class CarBooking(Base):
    __tablename__ = "car_bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    title = Column(String(length=255))
    place = Column(String(length=255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    origin = Column(String(length=255))
    destination = Column(String(length=255))
    distance = Column(Float)
    number_of_people = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow())
    status = Column(String(length=255), default="pending")
    is_deleted = Column(Boolean, default=False)
    CheckConstraint("start_time < end_time", name="time_constraint")

    car = relationship("Car", back_populates="car_bookings")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255))
    is_deleted = Column(Boolean, default=False)

    buying_requests = relationship("BuyingRequest", back_populates="department")


class Process(Base):
    __tablename__ = "processes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255))

    step = relationship("ProcessStep", back_populates="process")


class ProcessStep(Base):
    __tablename__ = "process_steps"

    process_id = Column(Integer, ForeignKey("processes.id"), primary_key=True, index=True)
    step = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    role = Column(String(length=255))
    approve_status = Column(String(length=255))
    deny_status = Column(String(length=255))

    process = relationship("Process", back_populates="step")
    buying_requests = relationship("BuyingRequest", back_populates="step")


class BuyingRequest(Base):
    __tablename__ = "buying_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    process_id = Column(Integer, ForeignKey("processes.id"))
    process_step = Column(Integer)
    title = Column(String(length=255))
    description = Column(String(length=500))
    approve_before = Column(DateTime)
    place = Column(String(length=255))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow())
    status = Column(String(length=255), default="pending")
    is_done = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    department = relationship("Department", back_populates="buying_requests")
    step = relationship("ProcessStep", back_populates="buying_requests")

    __table_args__ = (
        ForeignKeyConstraint(
            [process_id, process_step], [ProcessStep.process_id, ProcessStep.step]
        ),
    )


Base.metadata.create_all(engine)
