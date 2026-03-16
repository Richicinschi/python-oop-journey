"""Solution for Problem 05: Hotel Booking Model.

Demonstrates class design principles:
- Value Objects: RoomType encapsulates pricing logic
- Entity Objects: Room and Guest have unique identities
- Aggregates: Booking groups related entities
- Domain Logic: Room availability checking
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
        self._guest_id = guest_id
        self._name = name
        self._email = email
        self._phone = phone
    
    @property
    def guest_id(self) -> str:
        return self._guest_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def phone(self) -> str:
        return self._phone


class RoomType:
    """Room category with pricing.
    
    Attributes:
        category: Type category
        base_rate: Nightly rate
        description: Type description
    """
    
    def __init__(self, category: RoomTypeCategory, base_rate: float, description: str) -> None:
        self._category = category
        self._base_rate = base_rate
        self._description = description
    
    @property
    def category(self) -> RoomTypeCategory:
        return self._category
    
    @property
    def base_rate(self) -> float:
        return self._base_rate
    
    @property
    def description(self) -> str:
        return self._description
    
    def get_rate_for_date(self, date: date) -> float:
        """Get rate for a specific date (could vary by season)."""
        # Weekend surcharge
        if date.weekday() >= 5:  # Saturday=5, Sunday=6
            return self._base_rate * 1.2
        return self._base_rate


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
        self._room_number = room_number
        self._room_type = room_type
        self._floor = floor
        self._amenities = amenities or set()
    
    @property
    def room_number(self) -> str:
        return self._room_number
    
    @property
    def room_type(self) -> RoomType:
        return self._room_type
    
    @property
    def floor(self) -> int:
        return self._floor
    
    @property
    def amenities(self) -> set[Amenity]:
        return self._amenities.copy()
    
    def has_amenity(self, amenity: Amenity) -> bool:
        """Check if room has specific amenity."""
        return amenity in self._amenities
    
    def add_amenity(self, amenity: Amenity) -> None:
        """Add an amenity to the room."""
        self._amenities.add(amenity)
    
    def calculate_rate_for_dates(self, check_in: date, check_out: date) -> float:
        """Calculate total rate for date range."""
        total = 0.0
        current = check_in
        while current < check_out:
            total += self._room_type.get_rate_for_date(current)
            current += timedelta(days=1)
        return total


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
        if check_out <= check_in:
            raise ValueError("Check-out must be after check-in")
        
        self._booking_id = booking_id
        self._guest = guest
        self._room = room
        self._check_in = check_in
        self._check_out = check_out
        self._is_cancelled = False
    
    @property
    def booking_id(self) -> str:
        return self._booking_id
    
    @property
    def guest(self) -> Guest:
        return self._guest
    
    @property
    def room(self) -> Room:
        return self._room
    
    @property
    def check_in(self) -> date:
        return self._check_in
    
    @property
    def check_out(self) -> date:
        return self._check_out
    
    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled
    
    @property
    def nights(self) -> int:
        """Number of nights booked."""
        return (self._check_out - self._check_in).days
    
    @property
    def total_price(self) -> float:
        """Total price for the stay."""
        return self._room.calculate_rate_for_dates(self._check_in, self._check_out)
    
    def cancel(self) -> None:
        """Cancel the booking."""
        self._is_cancelled = True
    
    def overlaps_with(self, check_in: date, check_out: date) -> bool:
        """Check if booking overlaps with date range.
        
        Args:
            check_in: Start of date range
            check_out: End of date range
            
        Returns:
            True if dates overlap with this booking
        """
        if self._is_cancelled:
            return False
        # Two ranges overlap if neither ends before the other starts
        return not (check_out <= self._check_in or check_in >= self._check_out)
    
    def get_date_range(self) -> list[date]:
        """Get list of all dates in booking range."""
        dates = []
        current = self._check_in
        while current < self._check_out:
            dates.append(current)
            current += timedelta(days=1)
        return dates


class Hotel:
    """Hotel managing rooms and bookings.
    
    Attributes:
        name: Hotel name
        address: Hotel address
    """
    
    def __init__(self, name: str, address: str) -> None:
        self._name = name
        self._address = address
        self._rooms: list[Room] = []
        self._bookings: list[Booking] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def address(self) -> str:
        return self._address
    
    def add_room(self, room: Room) -> None:
        """Add a room to the hotel."""
        self._rooms.append(room)
    
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
        available = []
        for room in self._rooms:
            # Check room type filter
            if room_type and room.room_type != room_type:
                continue
            
            # Check amenities filter
            if required_amenities:
                if not required_amenities.issubset(room.amenities):
                    continue
            
            # Check availability
            if self._is_room_available(room, check_in, check_out):
                available.append(room)
        
        return available
    
    def _is_room_available(self, room: Room, check_in: date, check_out: date) -> bool:
        """Check if room has no overlapping bookings."""
        for booking in self._bookings:
            if booking.room == room and booking.overlaps_with(check_in, check_out):
                return False
        return True
    
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
        if not self._is_room_available(room, check_in, check_out):
            return None
        
        booking = Booking(booking_id, guest, room, check_in, check_out)
        self._bookings.append(booking)
        return booking
    
    def cancel_booking(self, booking: Booking) -> bool:
        """Cancel a booking.
        
        Args:
            booking: Booking to cancel
            
        Returns:
            True if cancelled successfully
        """
        if booking in self._bookings:
            booking.cancel()
            return True
        return False
    
    def get_guest_bookings(self, guest: Guest) -> list[Booking]:
        """Get all bookings for a guest."""
        return [b for b in self._bookings if b.guest == guest]
