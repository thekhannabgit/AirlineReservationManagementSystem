from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

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

class Aircraft(Base):
    __tablename__ = 'aircraft'
    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    manufacturer = Column(String(50))
    flights = relationship("Flight", back_populates="aircraft")

class Airport(Base):
    __tablename__ = 'airport'
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
    __tablename__ = 'crew_assignment'
    id = Column(Integer, primary_key=True)
    crew_id = Column(Integer, ForeignKey('crew.id'))
    flight_id = Column(Integer, ForeignKey('flight.id'))
    crew = relationship("Crew", back_populates="assignments")
    flight = relationship("Flight", back_populates="crew_assignments")

class Flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True)
    flight_number = Column(String(10), unique=True, nullable=False)
    departure_airport_code = Column(String(3), ForeignKey('airport.code'))
    arrival_airport_code = Column(String(3), ForeignKey('airport.code'))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    aircraft_id = Column(Integer, ForeignKey('aircraft.id'))
    status = Column(Enum(FlightStatus), default=FlightStatus.SCHEDULED)
    base_price = Column(Float, nullable=False)
    departure_airport = relationship("Airport", foreign_keys=[departure_airport_code], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_airport_code], back_populates="arriving_flights")
    aircraft = relationship("Aircraft", back_populates="flights")
    bookings = relationship("Booking", back_populates="flight")
    crew_assignments = relationship("CrewAssignment", back_populates="flight")

class Passenger(Base):
    __tablename__ = 'passenger'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    passport_number = Column(String(20))
    bookings = relationship("Booking", back_populates="passenger")

class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    passenger_id = Column(Integer, ForeignKey('passenger.id'))
    booking_date = Column(DateTime)
    seat_class = Column(String(20))
    status = Column(String(20))
    flight = relationship("Flight", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")