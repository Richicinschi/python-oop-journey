"""Problem 05: Hotel Booking Model.

Topic: Class Design Principles
Difficulty: Medium

Design a hotel booking system with the following classes:
- Guest: Hotel guest with contact information
- RoomType: Room category (single, double, suite) with pricing
- Room: Individual hotel room with number, type, and amenities
- Booking: Reservation linking guest, room, and dates
- Hotel: Manages rooms and bookings

Requirements:
- Rooms have types with different base rates
- Rooms can have amenities (wifi, balcony, etc.)
- Bookings have check-in/check-out dates
- Hotel checks room availability for date ranges
- Bookings calculate total price based on nights and room rate
- Cancellation releases room for those dates

Hints:
    - Hint 1: Hotel tracks bookings list; is_room_available checks for overlapping date ranges
    - Hint 2: Booking.total_price = (check_out - check_in).days * room.room_type.base_rate
    - Hint 3: Date overlap check: not (booking.check_out <= new_check_in or booking.check_in >= new_check_out)
"""

from __future__ import annotations

from datetime import date, timedelta
from enum import Enum, auto


class RoomTypeCategory(Enum):
    """Categories of hotel rooms."""
    SINGLE = auto()
    DOUBLE = auto()
    SUITE = auto()
    DELUXE = auto()


class Amenity(Enum):
    """Room amenities."""
    WIFI = auto()
    BALCONY = auto()
    MINIBAR = auto()
    SEA_VIEW = auto()
    ROOM_SERVICE = auto()
    JACUZZI = auto()


class Guest:
    """Hotel guest.
    
    Attributes:
        guest_id: Unique guest identifier
        name: Guest name
        email: Contact email
        phone: Contact phone
    """
    
    def __init__(self, guest_id: str, name: str, email: str, phone: str = "") -> None:
        raise NotImplementedError("Implement Guest.__init__")


class RoomType:
    """Room category with pricing.
    
    Attributes:
        category: Type category
        base_rate: Nightly rate
        description: Type description
    """
    
    def __init__(self, category: RoomTypeCategory, base_rate: float, description: str) -> None:
        raise NotImplementedError("Implement RoomType.__init__")
    
    def get_rate_for_date(self, date: date) -> float:
        """Get rate for a specific date (could vary by season)."""
        raise NotImplementedError("Implement RoomType.get_rate_for_date")


class Room:
    """Individual hotel room.
    
    Attributes:
        room_number: Room identifier
        room_type: Room category
        floor: Floor number
        amenities: Set of room amenities
    """
    
    def __init__(
        self,
        room_number: str,
        room_type: RoomType,
        floor: int,
        amenities: set[Amenity] | None = None
    ) -> None:
        raise NotImplementedError("Implement Room.__init__")
    
    def has_amenity(self, amenity: Amenity) -> bool:
        """Check if room has specific amenity."""
        raise NotImplementedError("Implement Room.has_amenity")
    
    def add_amenity(self, amenity: Amenity) -> None:
        """Add an amenity to the room."""
        raise NotImplementedError("Implement Room.add_amenity")
    
    def calculate_rate_for_dates(self, check_in: date, check_out: date) -> float:
        """Calculate total rate for date range."""
        raise NotImplementedError("Implement Room.calculate_rate_for_dates")


class Booking:
    """Room reservation.
    
    Attributes:
        booking_id: Unique booking identifier
        guest: Guest making the booking
        room: Room being booked
        check_in: Arrival date
        check_out: Departure date
        is_cancelled: Whether booking was cancelled
    """
    
    def __init__(
        self,
        booking_id: str,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date
    ) -> None:
        raise NotImplementedError("Implement Booking.__init__")
    
    @property
    def nights(self) -> int:
        """Number of nights booked."""
        raise NotImplementedError("Implement Booking.nights")
    
    @property
    def total_price(self) -> float:
        """Total price for the stay."""
        raise NotImplementedError("Implement Booking.total_price")
    
    def cancel(self) -> None:
        """Cancel the booking."""
        raise NotImplementedError("Implement Booking.cancel")
    
    def overlaps_with(self, check_in: date, check_out: date) -> bool:
        """Check if booking overlaps with date range.
        
        Args:
            check_in: Start of date range
            check_out: End of date range
            
        Returns:
            True if dates overlap with this booking
        """
        raise NotImplementedError("Implement Booking.overlaps_with")
    
    def get_date_range(self) -> list[date]:
        """Get list of all dates in booking range."""
        raise NotImplementedError("Implement Booking.get_date_range")


class Hotel:
    """Hotel managing rooms and bookings.
    
    Attributes:
        name: Hotel name
        address: Hotel address
    """
    
    def __init__(self, name: str, address: str) -> None:
        raise NotImplementedError("Implement Hotel.__init__")
    
    def add_room(self, room: Room) -> None:
        """Add a room to the hotel."""
        raise NotImplementedError("Implement Hotel.add_room")
    
    def find_available_rooms(
        self,
        check_in: date,
        check_out: date,
        room_type: RoomType | None = None,
        required_amenities: set[Amenity] | None = None
    ) -> list[Room]:
        """Find available rooms for date range.
        
        Args:
            check_in: Arrival date
            check_out: Departure date
            room_type: Optional room type filter
            required_amenities: Optional amenity requirements
            
        Returns:
            List of available rooms
        """
        raise NotImplementedError("Implement Hotel.find_available_rooms")
    
    def create_booking(
        self,
        booking_id: str,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date
    ) -> Booking | None:
        """Create a new booking.
        
        Args:
            booking_id: Unique booking ID
            guest: Guest making booking
            room: Room to book
            check_in: Arrival date
            check_out: Departure date
            
        Returns:
            Booking if successful, None if room unavailable
        """
        raise NotImplementedError("Implement Hotel.create_booking")
    
    def cancel_booking(self, booking: Booking) -> bool:
        """Cancel a booking.
        
        Args:
            booking: Booking to cancel
            
        Returns:
            True if cancelled successfully
        """
        raise NotImplementedError("Implement Hotel.cancel_booking")
    
    def get_guest_bookings(self, guest: Guest) -> list[Booking]:
        """Get all bookings for a guest."""
        raise NotImplementedError("Implement Hotel.get_guest_bookings")
