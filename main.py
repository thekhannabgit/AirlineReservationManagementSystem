# main.py
from database.initialization import initialize_database
from sqlalchemy.orm import sessionmaker
from presentation.app import AirlineApp
from sqlalchemy import text


def main():
    try:
        print("Initializing database...")
        engine = initialize_database()

        # Verify connection using ORM
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if flights exist using ORM - query all flights first
        from database.models import Flight
        all_flights = session.query(Flight).all()
        print(f"Database initialized successfully. Found {len(all_flights)} flights.")

        # If you specifically want to check if any flights exist
        first_flight = session.query(Flight).first()
        if first_flight:
            print(f"First flight: {first_flight.flight_number}")
        else:
            print("No flights found in database")

        print("Starting application...")
        app = AirlineApp(session)
        app.mainloop()

    except Exception as e:
        print(f"Application failed to start: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'session' in locals():
            session.close()
        print("Application shutdown")


if __name__ == "__main__":
    main()