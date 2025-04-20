import pytest
from database.models import Base, Aircraft
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_aircraft_creation(session):
    aircraft = Aircraft(model="Boeing 747", capacity=400)
    session.add(aircraft)
    session.commit()
    assert aircraft.id is not None