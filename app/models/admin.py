from sqladmin import ModelView
from app.models.user import User
from app.models.booking import Booking

class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.first_name,
        User.last_name,
        User.email,
        User.password,
        User.is_active,
        User.role,
        User.created_at,
        User.updated_at,
    ]

class BookingAdmin(ModelView, model=Booking):
    column_list = [
        Booking.id,
        Booking.booking_date,
        Booking.description,
        Booking.status,
        Booking.user_id,
        Booking.is_active,
        Booking.created_at,
        Booking.updated_at,
    ]