
import os
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from business_logic.auth_services import AuthService
from database import Base
from database.models import User, Airport, Aircraft, Flight, FlightStatus, UserRole, Passenger


def execute_sql_schema(engine):
    schema_file = os.path.abspath('database/schema.sql')
    with open(schema_file, 'r') as file:
        ddl_statements = file.read()

    raw_conn = engine.raw_connection()
    try:
        cursor = raw_conn.cursor()
        cursor.executescript(ddl_statements)
        raw_conn.commit()
    finally:
        raw_conn.close()


def initialize_database():
    # Ensure the database directory exists
    os.makedirs('database', exist_ok=True)

    # Database path
    db_path = os.path.abspath('database/skylink_db.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')

    # Execute raw schema SQL file to create tables
    execute_sql_schema(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create sample data if database is empty
    if not session.query(User).first():
        # Create sample airports
        airports = [
            Airport(code="JFK", name="John F. Kennedy", city="New York", country="USA"),
            Airport(code="LHR", name="Heathrow", city="London", country="UK"),
            Airport(code="DXB", name="Dubai International", city="Dubai", country="UAE")
        ]
        session.add_all(airports)

        # Create sample aircraft
        aircrafts = [
            Aircraft(model="Boeing 737", capacity=150, manufacturer="Boeing"),
            Aircraft(model="Airbus A320", capacity=180, manufacturer="Airbus")
        ]
        session.add_all(aircrafts)

        # Create sample flights
        flights = [
            Flight(
                flight_number="SK101",
                departure_airport_code="JFK",
                arrival_airport_code="LHR",
                departure_time=datetime.now() + timedelta(days=1),
                arrival_time=datetime.now() + timedelta(days=1, hours=7),
                aircraft_id=1,
                base_price=450.00,
                status=FlightStatus.SCHEDULED
            ),
            Flight(
                flight_number="SK202",
                departure_airport_code="LHR",
                arrival_airport_code="JFK",
                departure_time=datetime.now() + timedelta(days=2),
                arrival_time=datetime.now() + timedelta(days=2, hours=7),
                aircraft_id=2,
                base_price=460.00,
                status=FlightStatus.SCHEDULED
            )
        ]
        session.add_all(flights)

        # Create admin user
        auth_service = AuthService(session)
        auth_service.register_user(
            username="admin",
            password="admin123",
            email="admin@skylink.com",
            role=UserRole.ADMIN
        )
        passenger = Passenger(
            first_name="Admin",
            last_name="User",
            email="admin@skylink.com",
            phone="1234567890",
            passport_number="ADMIN123"
        )
        session.add(passenger)

        session.commit()

        # Create crew user
        auth_service = AuthService(session)
        auth_service.register_user(
            username="crew",
            password="crew123",
            email="crew@skylink.com",
            role=UserRole.STAFF
        )
        passenger = Passenger(
            first_name="Crew",
            last_name="User",
            email="crew@skylink.com",
            phone="2234567890",
            passport_number="CREW123"
        )
        session.add(passenger)

        session.commit()

    return engine
