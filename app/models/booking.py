from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Text
from enum import Enum as PythonEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from .common import CommonModel

class BookingStatus(str, PythonEnum):
	pending = "pending"
	approved = "approved"
	rejected = "rejected"

class Booking(CommonModel):
	__tablename__ = "bookings"

	booking_date = Column(DateTime, nullable=False)
	description = Column(Text, nullable=True)
	status = Column(Enum(BookingStatus), default=BookingStatus.pending)
	user_id = Column(String, ForeignKey("users.id"))
	user = relationship("User", back_populates="booking")

	def __repr__(self):
		return f"{self.email}"
	
metadata = Base.metadata