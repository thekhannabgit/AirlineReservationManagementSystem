import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from business_logic.flight_services import FlightService
from business_logic.booking_services import BookingService
from business_logic.crew_services import CrewService
from database.models import Base, Flight, Aircraft, Airport
from datetime import datetime, timedelta


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create test data
    aircraft = Aircraft(model="Boeing 737", capacity=150)
    session.add(aircraft)

    airports = [
        Airport(code="JFK", name="JFK International", city="New York", country="USA"),
        Airport(code="LHR", name="Heathrow", city="London", country="UK")
    ]
    session.add_all(airports)

    flight = Flight(
        flight_number="SK101",
        departure_airport_code="JFK",
        arrival_airport_code="LHR",
        departure_time=datetime.now() + timedelta(days=1),
        arrival_time=datetime.now() + timedelta(days=1, hours=7),
        aircraft_id=1,
        base_price=450.00
    )
    session.add(flight)
    session.commit()

    yield session
    session.close()


def test_flight_service_schedule_flight(db_session):
    service = FlightService(db_session)

    new_flight = {
        'flight_number': 'SK202',
        'departure_airport': 'LHR',
        'arrival_airport': 'JFK',
        'departure_time': (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
        'arrival_time': (datetime.now() + timedelta(days=2, hours=7)).strftime("%Y-%m-%d %H:%M"),
        'aircraft_id': 1,
        'base_price': 500.00
    }

    result = service.schedule_flight(new_flight)
    assert result.id is not None
    assert result.flight_number == 'SK202'


def test_booking_service_create_booking(db_session):
    booking_service = BookingService(db_session)

    booking_data = {
        'flight_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'passport_number': 'AB123456',
        'seat_class': 'Economy',
        'booking_date': datetime.now()
    }

    booking = booking_service.create_booking(booking_data)
    assert booking.id is not None
    assert booking.passenger.first_name == 'John'


def test_crew_service_assign_crew(db_session):
    from database.models import Crew

    # Add test crew member
    crew = Crew(name="Sarah Smith", role="Pilot", email="sarah@skylink.com")
    db_session.add(crew)
    db_session.commit()

    service = CrewService(db_session)
    result = service.assign_crew_to_flight(crew_id=1, flight_id=1)
    assert result is True


def test_reporting_service_trends():
    from unittest.mock import Mock
    from business_logic.reporting_services import ReportingService

    # Mock the analytics DAO
    mock_dao = Mock()
    mock_dao.get_booking_trends.return_value = [
        {'_id': '2023-01-01', 'count': 10, 'total_revenue': 4500},
        {'_id': '2023-01-02', 'count': 15, 'total_revenue': 6750}
    ]

    # Inject mock into service
    service = ReportingService()
    service.analytics_dao = mock_dao

    trends = service.get_booking_trends(days=7)
    assert len(trends) == 2
    assert trends[0]['count'] == 10