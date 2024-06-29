from fastapi import HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta, timezone

# from sqlalchemy.orm import Session

# from auth import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt

# import 
from app.models import booking as BookingModel
from app.schemas.booking import Booking, BookingCreate, BookingUpdate, BookingUpdateByAdmin
from app.schemas.user import User
from app.core.settings import SECRET_KEY, ALGORITHM
# from app.core.dependencies import get_db, oauth2_scheme
from app.api.endpoints.user import functions as user_functions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # get booking by id
# def get_booking_by_id( booking_id: str):
#     db_booking = db.query(BookingModel.Booking).filter(BookingModel.Booking.id == booking_id).first()
#     if db_booking is None:
#         raise HTTPException(status_code=404, detail="Booking not found")
#     return db_booking

# crete new booking
async def create_new_booking(booking: BookingCreate, current_user: User):
    loggedin_user= await user_functions.get_user_by_id(current_user.id)
    new_booking = BookingModel.Booking(
        booking_date=booking.booking_date, 
        description=booking.description, 
        user=loggedin_user)
    await new_booking.insert()
    return new_booking

# get my all bookings 
async def read_my_bookings(skip: int, limit: int, current_user:User):
    my_bookings = await BookingModel.Booking.find(BookingModel.Booking.user.id==current_user.id, with_children=True).skip(skip).limit(limit).to_list()
    return my_bookings

# get all bookings 
async def read_all_bookings(skip: int, limit: int):
    bookings = await BookingModel.Booking.all().skip(skip).limit(limit).to_list()
    return bookings



# update my booking
async def update_my_booking(booking_id: str, booking: BookingUpdate):
    db_booking = await BookingModel.Booking.get(booking_id)
    updated_data = booking.model_dump(exclude_unset=True) 
    for key, value in updated_data.items():
        setattr(db_booking, key, value)
    await db_booking.save()
    return db_booking

# update booking by admin
async def update_booking_by_admin(booking_id: str, booking: BookingUpdateByAdmin):
    db_booking = await BookingModel.Booking.get(booking_id)
    updated_data = booking.model_dump(exclude_unset=True) 
    for key, value in updated_data.items():
        setattr(db_booking, key, value)
    await db_booking.save()
    return db_booking

