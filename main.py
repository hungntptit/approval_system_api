from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import users, rooms, room_bookings, car_bookings, departments, cars, buying_requests

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

app.include_router(rooms.router)
app.include_router(room_bookings.router)

app.include_router(cars.router)
app.include_router(car_bookings.router)

app.include_router(departments.router)
app.include_router(buying_requests.router)