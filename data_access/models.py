# data_access/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data_access.db_session import Base
from datetime import datetime

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    flight_number = Column(String, unique=True)
    source = Column(String)
    destination = Column(String)
    departure_time = Column(DateTime)
    capacity = Column(Integer)
    bookings = relationship("Booking", back_populates="flight")

class Passenger(Base):
    __tablename__ = 'passengers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    bookings = relationship("Booking", back_populates="passenger")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    booking_ref = Column(String, unique=True)
    flight_id = Column(Integer, ForeignKey('flights.id'))
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    seat_number = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    flight = relationship("Flight", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")

class Crew(Base):
    __tablename__ = 'crew'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    flight_number = Column(String)
