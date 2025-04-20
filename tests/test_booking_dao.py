import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from data_access.booking_dao import BookingDAO
from datetime import datetime


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_booking(db_session):
    dao = BookingDAO(db_session)

    # First need to add a flight and passenger
    from database.models import Flight, Passenger
    flight = Flight(
        flight_number="TEST123",
        departure_airport_code="TEST",
        arrival_airport_code="TEST",
        departure_time=datetime.now(),
        arrival_time=datetime.now(),
        aircraft_id=1,
        base_price=100.00
    )
    db_session.add(flight)
    db_session.commit()

    passenger_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@test.com',
        'phone': '1234567890',
        'passport_number': 'TEST123456'
    }

    booking = dao.create_booking(flight.id, passenger_data, "Economy")
    assert booking is not None
    assert booking.id is not None
    assert booking.status == "Confirmed"