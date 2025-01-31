# from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Text
# from enum import Enum as PythonEnum
# from sqlalchemy.orm import relationship
# from app.core.database import Base
# from .common import CommonModel

# class BookingStatus(str, PythonEnum):
# 	pending = "pending"
# 	approved = "approved"
# 	rejected = "rejected"

# class Booking(CommonModel):
# 	__tablename__ = "bookings"

# 	booking_date = Column(DateTime, nullable=False)
# 	description = Column(Text, nullable=True)
# 	status = Column(Enum(BookingStatus), default=BookingStatus.pending)
# 	user_id = Column(String, ForeignKey("users.id"))
# 	user = relationship("User", back_populates="booking")

# 	def __repr__(self):
# 		return f"{self.email}"
	
# metadata = Base.metadata

from enum import Enum as PythonEnum
from typing import Optional
from datetime import datetime
from beanie import Document, Link
from pydantic import Field
from .common import CommonModel
from .user import User

class BookingStatus(str, PythonEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Booking(CommonModel):
    booking_date: datetime = Field(...)
    description: Optional[str] = Field(None)
    status: BookingStatus = Field(default=BookingStatus.pending)
    user: Link[User]

    class Settings:
        name = "bookings"

