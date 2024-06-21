from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.booking import BookingStatus
from .user import User

class BookingBase(BaseModel):
	booking_date: datetime
	description: str or None = None

class BookingCreate(BookingBase):
	pass

class BookingUpdate(BookingBase):
	pass

class Booking(BaseModel):
	id: str
	booking_date: datetime
	description: Optional[str]
	status: Optional[str]
	user: Optional[User]
	is_active: bool
	created_at: datetime
	updated_at: datetime




