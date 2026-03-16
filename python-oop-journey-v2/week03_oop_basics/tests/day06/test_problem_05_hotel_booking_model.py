"""Tests for Problem 05: Hotel Booking Model."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from week03_oop_basics.solutions.day06.problem_05_hotel_booking_model import (
    Amenity,
    Booking,
    Guest,
    Hotel,
    Room,
    RoomType,
    RoomTypeCategory,
)


class TestGuest:
    """Tests for Guest class."""
    
    def test_guest_creation(self) -> None:
        """Test guest initialization."""
        guest = Guest("G001", "John Smith", "john@example.com", "555-0123")
        assert guest.guest_id == "G001"
        assert guest.name == "John Smith"
        assert guest.email == "john@example.com"
        assert guest.phone == "555-0123"


class TestRoomType:
    """Tests for RoomType class."""
    
    def test_room_type_creation(self) -> None:
        """Test room type initialization."""
        room_type = RoomType(RoomTypeCategory.DOUBLE, 150.0, "Standard double room")
        assert room_type.category == RoomTypeCategory.DOUBLE
        assert room_type.base_rate == 150.0
        assert room_type.description == "Standard double room"
    
    def test_weekday_rate(self) -> None:
        """Test weekday rate (no surcharge)."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        # Monday = 0
        monday = date(2024, 1, 1)  # This is a Monday
        assert room_type.get_rate_for_date(monday) == 100.0
    
    def test_weekend_rate(self) -> None:
        """Test weekend rate (with surcharge)."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        # Saturday = 5
        saturday = date(2024, 1, 6)  # This is a Saturday
        assert room_type.get_rate_for_date(saturday) == 120.0


class TestRoom:
    """Tests for Room class."""
    
    def test_room_creation(self) -> None:
        """Test room initialization."""
        room_type = RoomType(RoomTypeCategory.DOUBLE, 150.0, "Double room")
        room = Room("101", room_type, 1, {Amenity.WIFI, Amenity.BALCONY})
        
        assert room.room_number == "101"
        assert room.room_type == room_type
        assert room.floor == 1
        assert Amenity.WIFI in room.amenities
        assert Amenity.BALCONY in room.amenities
    
    def test_room_default_amenities(self) -> None:
        """Test room with no amenities."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        assert room.amenities == set()
    
    def test_has_amenity(self) -> None:
        """Test amenity check."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1, {Amenity.WIFI})
        
        assert room.has_amenity(Amenity.WIFI) is True
        assert room.has_amenity(Amenity.BALCONY) is False
    
    def test_add_amenity(self) -> None:
        """Test adding amenity."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        room.add_amenity(Amenity.SEA_VIEW)
        assert room.has_amenity(Amenity.SEA_VIEW) is True
    
    def test_calculate_rate_for_dates(self) -> None:
        """Test rate calculation for date range."""
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        # Monday to Wednesday (2 nights, both weekdays)
        check_in = date(2024, 1, 1)  # Monday
        check_out = date(2024, 1, 3)  # Wednesday
        
        assert room.calculate_rate_for_dates(check_in, check_out) == 200.0


class TestBooking:
    """Tests for Booking class."""
    
    def test_booking_creation(self) -> None:
        """Test booking initialization."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        check_in = date(2024, 1, 1)
        check_out = date(2024, 1, 5)
        
        booking = Booking("B001", guest, room, check_in, check_out)
        
        assert booking.booking_id == "B001"
        assert booking.guest == guest
        assert booking.room == room
        assert booking.is_cancelled is False
    
    def test_booking_invalid_dates(self) -> None:
        """Test booking with check-out before check-in."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        check_in = date(2024, 1, 5)
        check_out = date(2024, 1, 1)
        
        with pytest.raises(ValueError):
            Booking("B001", guest, room, check_in, check_out)
    
    def test_booking_nights(self) -> None:
        """Test nights calculation."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        check_in = date(2024, 1, 1)
        check_out = date(2024, 1, 5)
        
        booking = Booking("B001", guest, room, check_in, check_out)
        assert booking.nights == 4
    
    def test_booking_total_price(self) -> None:
        """Test total price calculation."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        check_in = date(2024, 1, 1)  # Monday
        check_out = date(2024, 1, 3)  # Wednesday
        
        booking = Booking("B001", guest, room, check_in, check_out)
        assert booking.total_price == 200.0  # 2 nights @ 100
    
    def test_cancel_booking(self) -> None:
        """Test booking cancellation."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        booking = Booking("B001", guest, room, date(2024, 1, 1), date(2024, 1, 5))
        booking.cancel()
        
        assert booking.is_cancelled is True
    
    def test_overlaps_with_true(self) -> None:
        """Test overlap detection - overlapping dates."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        booking = Booking("B001", guest, room, date(2024, 1, 5), date(2024, 1, 10))
        
        # Overlapping ranges
        assert booking.overlaps_with(date(2024, 1, 7), date(2024, 1, 12)) is True
        assert booking.overlaps_with(date(2024, 1, 1), date(2024, 1, 7)) is True
        assert booking.overlaps_with(date(2024, 1, 6), date(2024, 1, 8)) is True
    
    def test_overlaps_with_false(self) -> None:
        """Test overlap detection - non-overlapping dates."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        booking = Booking("B001", guest, room, date(2024, 1, 5), date(2024, 1, 10))
        
        # Non-overlapping ranges
        assert booking.overlaps_with(date(2024, 1, 1), date(2024, 1, 5)) is False
        assert booking.overlaps_with(date(2024, 1, 10), date(2024, 1, 15)) is False
    
    def test_overlaps_with_cancelled(self) -> None:
        """Test overlap detection - cancelled booking doesn't overlap."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        booking = Booking("B001", guest, room, date(2024, 1, 5), date(2024, 1, 10))
        booking.cancel()
        
        assert booking.overlaps_with(date(2024, 1, 6), date(2024, 1, 8)) is False
    
    def test_get_date_range(self) -> None:
        """Test getting list of dates in range."""
        guest = Guest("G001", "John Smith", "john@example.com")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        booking = Booking("B001", guest, room, date(2024, 1, 1), date(2024, 1, 4))
        dates = booking.get_date_range()
        
        assert len(dates) == 3
        assert dates[0] == date(2024, 1, 1)
        assert dates[1] == date(2024, 1, 2)
        assert dates[2] == date(2024, 1, 3)


class TestHotel:
    """Tests for Hotel class."""
    
    def test_hotel_creation(self) -> None:
        """Test hotel initialization."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        assert hotel.name == "Grand Hotel"
        assert hotel.address == "123 Main St"
    
    def test_add_room(self) -> None:
        """Test adding room to hotel."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        
        hotel.add_room(room)
        
        # Room should be available
        available = hotel.find_available_rooms(date(2024, 1, 1), date(2024, 1, 5))
        assert len(available) == 1
    
    def test_find_available_rooms_by_type(self) -> None:
        """Test filtering by room type."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        single_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        double_type = RoomType(RoomTypeCategory.DOUBLE, 150.0, "Double room")
        
        hotel.add_room(Room("101", single_type, 1))
        hotel.add_room(Room("102", double_type, 1))
        
        available = hotel.find_available_rooms(
            date(2024, 1, 1),
            date(2024, 1, 5),
            room_type=single_type
        )
        assert len(available) == 1
        assert available[0].room_number == "101"
    
    def test_find_available_rooms_by_amenity(self) -> None:
        """Test filtering by required amenities."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        
        hotel.add_room(Room("101", room_type, 1, {Amenity.WIFI}))
        hotel.add_room(Room("102", room_type, 1, {Amenity.WIFI, Amenity.BALCONY}))
        hotel.add_room(Room("103", room_type, 1, set()))
        
        available = hotel.find_available_rooms(
            date(2024, 1, 1),
            date(2024, 1, 5),
            required_amenities={Amenity.WIFI}
        )
        assert len(available) == 2
    
    def test_find_available_rooms_occupied(self) -> None:
        """Test room not available when booked."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        hotel.add_room(room)
        
        guest = Guest("G001", "John Smith", "john@example.com")
        hotel.create_booking("B001", guest, room, date(2024, 1, 5), date(2024, 1, 10))
        
        # Should not be available for overlapping dates
        available = hotel.find_available_rooms(date(2024, 1, 7), date(2024, 1, 12))
        assert len(available) == 0
        
        # Should be available for non-overlapping dates
        available = hotel.find_available_rooms(date(2024, 1, 10), date(2024, 1, 15))
        assert len(available) == 1
    
    def test_create_booking_success(self) -> None:
        """Test successful booking creation."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        hotel.add_room(room)
        
        guest = Guest("G001", "John Smith", "john@example.com")
        booking = hotel.create_booking("B001", guest, room, date(2024, 1, 1), date(2024, 1, 5))
        
        assert booking is not None
        assert booking.booking_id == "B001"
    
    def test_create_booking_unavailable(self) -> None:
        """Test booking when room unavailable."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        hotel.add_room(room)
        
        guest1 = Guest("G001", "John Smith", "john@example.com")
        guest2 = Guest("G002", "Jane Doe", "jane@example.com")
        
        hotel.create_booking("B001", guest1, room, date(2024, 1, 1), date(2024, 1, 10))
        
        # Second booking should fail
        booking = hotel.create_booking("B002", guest2, room, date(2024, 1, 5), date(2024, 1, 15))
        assert booking is None
    
    def test_cancel_booking(self) -> None:
        """Test booking cancellation."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room = Room("101", room_type, 1)
        hotel.add_room(room)
        
        guest = Guest("G001", "John Smith", "john@example.com")
        booking = hotel.create_booking("B001", guest, room, date(2024, 1, 1), date(2024, 1, 5))
        
        # Room should be occupied
        available = hotel.find_available_rooms(date(2024, 1, 2), date(2024, 1, 4))
        assert len(available) == 0
        
        # Cancel booking
        assert hotel.cancel_booking(booking) is True
        
        # Room should be available again
        available = hotel.find_available_rooms(date(2024, 1, 2), date(2024, 1, 4))
        assert len(available) == 1
    
    def test_get_guest_bookings(self) -> None:
        """Test getting bookings for a guest."""
        hotel = Hotel("Grand Hotel", "123 Main St")
        
        room_type = RoomType(RoomTypeCategory.SINGLE, 100.0, "Single room")
        room1 = Room("101", room_type, 1)
        room2 = Room("102", room_type, 1)
        hotel.add_room(room1)
        hotel.add_room(room2)
        
        guest = Guest("G001", "John Smith", "john@example.com")
        hotel.create_booking("B001", guest, room1, date(2024, 1, 1), date(2024, 1, 5))
        hotel.create_booking("B002", guest, room2, date(2024, 1, 10), date(2024, 1, 15))
        
        bookings = hotel.get_guest_bookings(guest)
        assert len(bookings) == 2
