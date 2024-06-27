from fastapi import HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

# from auth import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt

# import 
from app.models import booking as BookingModel
from app.schemas.booking import Booking, BookingCreate, BookingUpdate, BookingUpdateByAdmin
from app.schemas.user import User
from app.core.settings import SECRET_KEY, ALGORITHM
from app.core.dependencies import get_db, oauth2_scheme
from app.api.endpoints.user import functions as user_functions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# get booking by id
def get_booking_by_id(db: Session, booking_id: str):
    db_booking = db.query(BookingModel.Booking).filter(BookingModel.Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

# crete new booking
def create_new_booking(db: Session, booking: BookingCreate, current_user: User):
    new_booking = BookingModel.Booking(booking_date=booking.booking_date, description=booking.description, user_id=current_user.id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# get my bookings 
def read_my_bookings(db: Session, skip: int, limit: int, current_user:User):
    return db.query(BookingModel.Booking).filter(BookingModel.Booking.user_id == current_user.id).offset(skip).limit(limit).all()

# get my bookings 
def read_all_bookings(db: Session, skip: int, limit: int):
    return db.query(BookingModel.Booking).offset(skip).limit(limit).all()



# update my booking
def update_my_booking(db: Session, booking_id: str, booking: BookingUpdate):
    db_booking = get_booking_by_id(db, booking_id)
    updated_data = booking.model_dump(exclude_unset=True) 
    for key, value in updated_data.items():
        setattr(db_booking, key, value)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# update booking by admin
def update_booking_by_admin(db: Session, booking_id: str, booking: BookingUpdateByAdmin):
    db_booking = get_booking_by_id(db, booking_id)
    updated_data = booking.model_dump(exclude_unset=True) 
    for key, value in updated_data.items():
        setattr(db_booking, key, value)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

