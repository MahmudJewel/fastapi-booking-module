# # fastapi 
# from fastapi import APIRouter, Depends, HTTPException

# # sqlalchemy
# from sqlalchemy.orm import Session

# # import
# from app.core.dependencies import get_db, oauth2_scheme 
# from app.schemas.booking import Booking, BookingCreate, BookingUpdate, BookingUpdateByAdmin
# from app.api.endpoints.booking import functions as booking_functions
# from app.core.rolechecker import RoleChecker
# from app.api.endpoints.user import functions as user_functions
# from app.schemas.user import User

# booking_module = APIRouter()

# # create new booking 
# @booking_module.post('/', 
#                      response_model=Booking,
#                      dependencies=[Depends(RoleChecker(['user', 'admin']))]
#                      )
# async def create_new_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(user_functions.get_current_user)):
#     new_booking = booking_functions.create_new_booking(db, booking, current_user)
#     return new_booking

# # get my booking list 
# @booking_module.get('/', 
#             response_model=list[Booking],
#             dependencies=[Depends(RoleChecker(['admin', 'user']))]
#             )
# async def read_my_bookings( skip: int = 0, limit: int = 100,  db: Session = Depends(get_db), current_user: User = Depends(user_functions.get_current_user)):
#     return booking_functions.read_my_bookings(db, skip, limit, current_user)

# # get all booking list
# @booking_module.get('/all-booking/', 
#             response_model=list[Booking],
#             dependencies=[Depends(RoleChecker(['admin']))]
#             )
# async def read_all_booking( skip: int = 0, limit: int = 100,  db: Session = Depends(get_db)):
#     return booking_functions.read_all_bookings(db, skip, limit)





# fastapi 
from fastapi import APIRouter, Depends, HTTPException
from typing import List
# import
# from app.core.dependencies import get_db, oauth2_scheme 
from app.schemas.booking import Booking, BookingCreate, BookingUpdate, BookingUpdateByAdmin
from app.api.endpoints.booking import functions as booking_functions
from app.core.rolechecker import RoleChecker
from app.api.endpoints.user import functions as user_functions
from app.schemas.user import User

booking_module = APIRouter()

# get my booking list 
@booking_module.get('/', 
            # response_model=list[Booking],
            dependencies=[Depends(RoleChecker(['admin', 'user']))]
            )
async def read_my_bookings( skip: int = 0, limit: int = 100, current_user: User = Depends(user_functions.get_current_user)):
    return await booking_functions.read_my_bookings(skip, limit, current_user)

# get all booking list
@booking_module.get('/all-booking/', 
            # response_model=list[Booking],
            dependencies=[Depends(RoleChecker(['admin']))]
            )
async def read_all_booking( skip: int = 0, limit: int = 100):
    return await booking_functions.read_all_bookings(skip, limit)

# create new booking 
@booking_module.post('/', 
                     response_model=Booking,
                     )
async def create_new_booking(booking: BookingCreate, current_user: User = Depends(user_functions.get_current_user)):
    new_booking = await booking_functions.create_new_booking(booking, current_user)
    return new_booking

# update my booking
@booking_module.patch('/{booking_id}', 
            #   response_model=Booking,
              dependencies=[Depends(RoleChecker(['admin', 'user']))]
              )
async def update_my_booking( booking_id: str, booking: BookingUpdate):
    return await booking_functions.update_my_booking(booking_id, booking)

# update booking by admin
@booking_module.patch('/admin/{booking_id}', 
            #   response_model=Booking,
              dependencies=[Depends(RoleChecker(['admin']))]
              )
async def update_booking_by_admin( booking_id: str, booking: BookingUpdateByAdmin):
    return await booking_functions.update_booking_by_admin(booking_id, booking)

