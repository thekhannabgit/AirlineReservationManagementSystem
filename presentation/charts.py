# presentation/charts.py
import matplotlib.pyplot as plt
from data_access.models import Booking, Flight
from data_access.db_session import SessionLocal
from collections import Counter

def show_analytics_chart():
    session = SessionLocal()

    # Chart 1: Bookings per flight
    bookings = session.query(Booking).all()
    flight_ids = [b.flight_id for b in bookings]
    flight_count = Counter(flight_ids)

    flights = session.query(Flight).all()
    flight_labels = [f.flight_number for f in flights if f.id in flight_count]
    counts = [flight_count[f.id] for f in flights if f.id in flight_count]

    plt.figure(figsize=(10, 6))
    plt.bar(flight_labels, counts, color='skyblue')
    plt.title("Bookings per Flight")
    plt.xlabel("Flight Number")
    plt.ylabel("Number of Bookings")
    plt.tight_layout()
    plt.show()

    session.close()
