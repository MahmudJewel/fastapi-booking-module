from enum import Enum as PythonEnum
from typing import Optional, List
from beanie import Document, Indexed, Link
from pydantic import Field
from datetime import datetime
from .common import CommonModel
# from typing import List
class UserRole(str, PythonEnum):
    user = "user"
    admin = "admin"

class User(CommonModel):
    email: str = Field(max_length=50, unique=True)
    password: Optional[str] = Field(max_length=500, default=None)
    first_name: Optional[str] = Field(max_length=50, default=None)
    last_name: Optional[str] = Field(max_length=50, default=None)
    role: UserRole = Field(default=UserRole.user)
    bookings: List[Link["Booking"]] = []

    class Settings:
        collection = "users"
