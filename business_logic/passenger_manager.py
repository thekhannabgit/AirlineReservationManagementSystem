# business_logic/passenger_manager.py
from data_access.models import Passenger
from data_access.db_session import SessionLocal

def get_all_passengers():
    session = SessionLocal()
    passengers = session.query(Passenger).all()
    session.close()
    return passengers
