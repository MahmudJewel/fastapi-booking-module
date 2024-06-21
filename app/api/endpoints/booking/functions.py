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

# # get user by email 
# def get_user_by_email(db: Session, email: str):
#     return db.query(UserModel.User).filter(UserModel.User.email == email).first()

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



# # delete user
# def delete_user(db: Session, user_id: str):
#     db_user = get_user_by_id(db, user_id)
#     db.delete(db_user)
#     db.commit()
#     # db.refresh(db_user)
#     return {"msg": f"{db_user.email} deleted successfully"}

# # =====================> login/logout <============================
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def authenticate_user(db: Session, user: UserCreate):
#     member = get_user_by_email(db, user.email)
#     if not member:
#         return False
#     if not verify_password(user.password, member.password):
#         return False
#     return member

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # get current users info 
# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid authentication credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # print(f"Payload =====> {payload}")
#         current_email: str = payload.get("email")
#         if current_email is None:
#             raise credentials_exception
#         user = get_user_by_email(db, current_email)
#         if user is None:
#             raise credentials_exception
#         return user
#     except JWTError:
#         raise credentials_exception

