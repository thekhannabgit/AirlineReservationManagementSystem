# database/initialization.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Airport, Aircraft, Flight, Crew, CrewAssignment, FlightStatus, CrewRole
from datetime import datetime, timedelta

# database/initialization.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, UserRole
import os


def initialize_database():
    # Database setup
    os.makedirs('database', exist_ok=True)
    db_path = os.path.abspath('database/skylink_db.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')

    # Create tables
    Base.metadata.create_all(engine)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create admin user if not exists
    create_admin_user(session)

    return engine


def create_admin_user(session):
    admin = session.query(User).filter(User.username == "admin").first()
    if not admin:
        from business_logic.auth_services import AuthService
        auth_service = AuthService(session)
        auth_service.register_user(
            username="admin",
            password="admin123",  # Change this in production!
            email="admin@skylink.com",
            role=UserRole.ADMIN
        )
        print("Admin user created successfully")

'''def initialize_database():
    # Ensure the database directory exists
    os.makedirs('database', exist_ok=True)

    # Database path
    db_path = os.path.abspath('database/skylink_db.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')

    # Create all tables
    Base.metadata.create_all(engine)

    return engine'''


'''def initialize_database():
    # Ensure the database directory exists
    os.makedirs('database', exist_ok=True)

    # Database path - now in the database folder
    db_path = os.path.abspath('database/skylink_db.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')

    try:
        # Create all tables if they don't exist
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        # Only create sample data if the database is empty
        if not session.query(Airport).first():
            # Create sample data
            airports = [
                Airport(code="JFK", name="John F. Kennedy", city="New York", country="USA"),
                Airport(code="LHR", name="Heathrow", city="London", country="UK"),
                Airport(code="DXB", name="Dubai International", city="Dubai", country="UAE"),
                Airport(code="SIN", name="Changi", city="Singapore", country="Singapore")
            ]
            session.add_all(airports)

            # Aircraft
            aircrafts = [
                Aircraft(model="Boeing 737", capacity=150, manufacturer="Boeing"),
                Aircraft(model="Airbus A320", capacity=180, manufacturer="Airbus"),
                Aircraft(model="Boeing 787", capacity=250, manufacturer="Boeing")
            ]
            session.add_all(aircrafts)
            session.flush()

            # Crew
            crew_members = [
                Crew(first_name="John", last_name="Smith", email="john@skylink.com", role=CrewRole.PILOT),
                Crew(first_name="Sarah", last_name="Johnson", email="sarah@skylink.com",
                     role=CrewRole.FLIGHT_ATTENDANT),
                Crew(first_name="Michael", last_name="Brown", email="michael@skylink.com", role=CrewRole.COPILOT)
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
                    aircraft_id=aircrafts[0].id,
                    base_price=450.00,
                    status=FlightStatus.SCHEDULED
                ),
                Flight(
                    flight_number="SK202",
                    departure_airport_code="LHR",
                    arrival_airport_code="JFK",
                    departure_time=datetime.now() + timedelta(days=2),
                    arrival_time=datetime.now() + timedelta(days=2, hours=7),
                    aircraft_id=aircrafts[1].id,
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

        from business_logic.auth_services import AuthService
        Session = sessionmaker(bind=engine)
        session = Session()
        auth_service = AuthService(session)
        auth_service.create_admin_user()
        session.close()

        return engine

    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise'''