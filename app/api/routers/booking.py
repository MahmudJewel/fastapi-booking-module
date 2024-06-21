from fastapi import APIRouter
from app.api.endpoints.booking.booking import booking_module

booking_router = APIRouter()

booking_router.include_router(
    booking_module,
    prefix="/booking",
    tags=["bookings"],
    responses={404: {"description": "Not found"}},
)