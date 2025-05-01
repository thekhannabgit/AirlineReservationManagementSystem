import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Airport, Aircraft, Flight, Crew, CrewAssignment, FlightStatus, CrewRole
from datetime import datetime, timedelta


def initialize_database():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Database path
    db_path = os.path.abspath('data/skylink_db.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')

    try:
        # Drop all tables if they exist
        Base.metadata.drop_all(engine)

        # Create all tables
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        # Create sample data
        # Airports
        airports = [
            Airport(code="JFK", name="John F. Kennedy", city="New York", country="USA"),
            Airport(code="LHR", name="Heathrow", city="London", country="UK")
        ]
        session.add_all(airports)

        # Aircraft
        aircraft = Aircraft(model="Boeing 737", capacity=150, manufacturer="Boeing")
        session.add(aircraft)
        session.flush()

        # Crew
        crew_members = [
            Crew(first_name="John", last_name="Smith", email="john@skylink.com", role=CrewRole.PILOT),
            Crew(first_name="Sarah", last_name="Johnson", email="sarah@skylink.com", role=CrewRole.FLIGHT_ATTENDANT)
        ]
        session.add_all(crew_members)
        session.flush()

        # Flights
        flights = [
            Flight(
                flight_number="SK101",
                departure_airport_code="JFK",
                arrival_airport_code="LHR",
                departure_time=datetime.now() + timedelta(days=1),
                arrival_time=datetime.now() + timedelta(days=1, hours=7),
                aircraft_id=aircraft.id,
                base_price=450.00,
                status=FlightStatus.SCHEDULED
            ),
            Flight(
                flight_number="SK202",
                departure_airport_code="LHR",
                arrival_airport_code="JFK",
                departure_time=datetime.now() + timedelta(days=2),
                arrival_time=datetime.now() + timedelta(days=2, hours=7),
                aircraft_id=aircraft.id,
                base_price=460.00,
                status=FlightStatus.SCHEDULED
            )
        ]
        session.add_all(flights)
        session.flush()

        # Crew Assignments
        assignments = [
            CrewAssignment(crew_id=crew_members[0].id, flight_id=flights[0].id),
            CrewAssignment(crew_id=crew_members[1].id, flight_id=flights[0].id)
        ]
        session.add_all(assignments)

        session.commit()
        return engine

    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise