from database.initialization import initialize_database
from sqlalchemy.orm import sessionmaker
from presentation.app import AirlineApp
from database.sample_analytics import create_sample_analytics
from pymongo import MongoClient
from config import settings
import sys


def main():
    session = None  # Initialize session variable
    try:
        print("Initializing database...")
        engine = initialize_database()

        print("Creating sample analytics data...")
        create_sample_analytics()

        # Test MongoDB connection
        try:
            client = MongoClient(settings.MONGODB_URI)
            db = client["skylink_analytics"]
            print("MongoDB test connection successful!")
            print(f"Available collections: {db.list_collection_names()}")
            client.close()
        except Exception as e:
            print(f"MongoDB test connection failed: {e}")

        # Create SQLAlchemy session
        Session = sessionmaker(bind=engine)
        session = Session()

        print("Starting application...")
        app = AirlineApp(session)
        app.mainloop()

    except Exception as e:
        print(f"Application failed to start: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
    finally:
        if session is not None:  # Properly check if session exists
            session.close()
        print("Application shutdown")

def show_window(self, name):
    window = self.windows.get(name)
    if window:
        if hasattr(window, "on_show"):
            window.on_show()  # Refreshes data
        window.tkraise()

if __name__ == "__main__":
    main()