from sqlalchemy.orm import Session
from typing import List, Optional
from database.models import Passenger


class PassengerDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_passenger_by_email(self, email: str) -> Optional[Passenger]:
        return self.session.query(Passenger).filter(Passenger.email == email).first()

    def create_passenger(self, passenger_data: dict) -> Passenger:
        passenger = Passenger(
            first_name=passenger_data['first_name'],
            last_name=passenger_data['last_name'],
            email=passenger_data['email'],
            phone=passenger_data['phone'],
            passport_number=passenger_data['passport_number']
        )
        self.session.add(passenger)
        self.session.commit()
        return passenger