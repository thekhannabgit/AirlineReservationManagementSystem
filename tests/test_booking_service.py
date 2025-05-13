import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Flight, Aircraft, Airport, Passenger
from business_logic.booking_services import BookingService


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create test data
    airport1 = Airport(code="JFK", name="JFK", city="New York", country="USA")
    airport2 = Airport(code="LHR", name="Heathrow", city="London", country="UK")
    aircraft = Aircraft(model="Boeing 737", capacity=150)

    flight = Flight(
        flight_number="SK101",
        departure_airport_code="JFK",
        arrival_airport_code="LHR",
        departure_time=datetime.now() + timedelta(days=1),
        arrival_time=datetime.now() + timedelta(days=1, hours=7),
        aircraft_id=1,
        base_price=450.00
    )

    session.add_all([airport1, airport2, aircraft, flight])
    session.commit()

    yield session
    session.close()


def test_make_booking_success(db_session):
    service = BookingService(db_session)
    passenger_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'passport_number': 'AB123456'
    }

    booking = service.make_booking(1, passenger_data, "Economy")
    assert booking is not None
    assert booking.id is not None
    assert booking.passenger.first_name == 'John'
    assert booking.flight.flight_number == 'SK101'
    assert booking.status == 'Confirmed'


def test_make_booking_flight_full(db_session):
    service = BookingService(db_session)
    passenger_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'passport_number': 'AB123456'
    }

    # Fill all seats
    flight = db_session.query(Flight).first()
    flight.aircraft.capacity = 1  # Set capacity to 1 for test

    # First booking should succeed
    booking1 = service.make_booking(1, passenger_data, "Economy")
    assert booking1 is not None

    # Second booking should fail
    booking2 = service.make_booking(1, passenger_data, "Economy")
    assert booking2 is None