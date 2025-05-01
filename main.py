import os
from presentation.app import AirlineApp
from database.initialization import initialize_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text  # Added import


def main():
    try:
        print("Initializing database...")
        engine = initialize_database()

        # Verify connection and data using SQLAlchemy text() for raw SQL
        with engine.connect() as conn:
            print("Database connection successful")
            result = conn.execute(text("SELECT flight_number, status FROM flight"))
            for row in result:
                print(f"Flight {row.flight_number} - Status: {row.status}")

        Session = sessionmaker(bind=engine)
        session = Session()

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