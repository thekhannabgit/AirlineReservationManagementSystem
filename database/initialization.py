from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Aircraft, Airport, Flight, Passenger, Booking
from datetime import datetime, timedelta


def initialize_database():
    engine = create_engine('sqlite:///skylink_db.sqlite')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create sample data if empty
    if not session.query(Aircraft).first():
        # Sample aircrafts
        aircrafts = [
            Aircraft(model="Boeing 737-800", capacity=162, manufacturer="Boeing", year_of_manufacture=2018),
            Aircraft(model="Airbus A320", capacity=150, manufacturer="Airbus", year_of_manufacture=2019)
        ]
        session.add_all(aircrafts)

        # Sample airports
        airports = [
            Airport(code="LHR", name="Heathrow Airport", city="London", country="UK"),
            Airport(code="JFK", name="John F. Kennedy International", city="New York", country="USA")
        ]
        session.add_all(airports)

        session.commit()

        # Sample flights
        now = datetime.now()
        flights = [
            Flight(
                flight_number="SK101",
                departure_airport_code="LHR",
                arrival_airport_code="JFK",
                departure_time=now + timedelta(days=1),
                arrival_time=now + timedelta(days=1, hours=7),
                aircraft_id=1,
                base_price=450.00
            )
        ]
        session.add_all(flights)
        session.commit()

    return engine