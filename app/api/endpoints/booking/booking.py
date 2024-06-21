# fastapi 
from fastapi import APIRouter, Depends, HTTPException

# sqlalchemy
from sqlalchemy.orm import Session

# import
from app.core.dependencies import get_db, oauth2_scheme 
from app.schemas.booking import Booking, BookingCreate #, UserUpdate
from app.api.endpoints.booking import functions as booking_functions
from app.core.rolechecker import RoleChecker

booking_module = APIRouter()

# create new booking 
@booking_module.post('/', 
                     response_model=Booking,
                     # dependencies=[Depends(RoleChecker(['admin']))]
                     )
async def create_new_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    new_booking = booking_functions.create_new_booking(db, booking)
    return new_booking

# get all bookings 
@booking_module.get('/', 
            response_model=list[Booking],
            dependencies=[Depends(RoleChecker(['admin', 'user']))]
            )
async def read_all_booking( skip: int = 0, limit: int = 100,  db: Session = Depends(get_db)):
    return booking_functions.read_all_booking(db, skip, limit)

# # get user by id 
# @user_module.get('/{user_id}', 
#             response_model=User,
#             # dependencies=[Depends(RoleChecker(['admin']))]
#             )
# async def read_user_by_id( user_id: str, db: Session = Depends(get_db)):
#     return user_functions.get_user_by_id(db, user_id)

# # update user
# @user_module.patch('/{user_id}', 
#               response_model=User,
#             #   dependencies=[Depends(RoleChecker(['admin']))]
#               )
# async def update_user( user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
#     print(f"Received data: {user.model_dump()}")
#     return user_functions.update_user(db, user_id, user)

# # delete user
# @user_module.delete('/{user_id}', 
#             #    response_model=User,
#             #    dependencies=[Depends(RoleChecker(['admin']))]
#                )
# async def delete_user( user_id: str, db: Session = Depends(get_db)):
#     deleted_user = user_functions.delete_user(db, user_id)
    
#     return deleted_user

