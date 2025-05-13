import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    USER = "User"

class FlightStatus(enum.Enum):
    SCHEDULED = "Scheduled"
    DELAYED = "Delayed"
    DEPARTED = "Departed"
    ARRIVED = "Arrived"
    CANCELLED = "Cancelled"

class CrewRole(enum.Enum):
    PILOT = "Pilot"
    COPILOT = "Co-Pilot"
    FLIGHT_ATTENDANT = "Flight Attendant"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

class Aircraft(Base):
    __tablename__ = 'aircrafts'
    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    manufacturer = Column(String(50))
    flights = relationship("Flight", back_populates="aircraft")

class Airport(Base):
    __tablename__ = 'airports'
    code = Column(String(3), primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    departing_flights = relationship("Flight", foreign_keys="Flight.departure_airport_code", back_populates="departure_airport")
    arriving_flights = relationship("Flight", foreign_keys="Flight.arrival_airport_code", back_populates="arrival_airport")

class Crew(Base):
    __tablename__ = 'crew'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100))
    role = Column(Enum(CrewRole))
    assignments = relationship("CrewAssignment", back_populates="crew")

class CrewAssignment(Base):
    __tablename__ = 'crew_assignments'
    id = Column(Integer, primary_key=True)
    crew_id = Column(Integer, ForeignKey('crew.id'))
    flight_id = Column(Integer, ForeignKey('flights.id'))
    crew = relationship("Crew", back_populates="assignments")
    flight = relationship("Flight", back_populates="crew_assignments")

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    flight_number = Column(String(10), unique=True, nullable=False)
    departure_airport_code = Column(String(3), ForeignKey('airports.code'))
    arrival_airport_code = Column(String(3), ForeignKey('airports.code'))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    aircraft_id = Column(Integer, ForeignKey('aircrafts.id'))
    status = Column(Enum(FlightStatus), default=FlightStatus.SCHEDULED)
    base_price = Column(Float, nullable=False)
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_code], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_code], back_populates="arriving_flights")
    aircraft = relationship("Aircraft", back_populates="flights")
    bookings = relationship("Booking", back_populates="flight")
    crew_assignments = relationship("CrewAssignment", back_populates="flight")

class Passenger(Base):
    __tablename__ = 'passengers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    passport_number = Column(String(20))
    bookings = relationship("Booking", back_populates="passenger")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.id'))
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    booking_date = Column(DateTime)
    seat_class = Column(String(20))
    status = Column(String(20))
    final_price = Column(Float)  # Added final_price field
    flight = relationship("Flight", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")