from datetime import datetime, timedelta
from pymongo import MongoClient
from config import settings
import random
import time


def create_sample_analytics():
    client = MongoClient(settings.MONGODB_URI)
    db = client["skylink_analytics"]

    # Clear existing data
    db.bookings.delete_many({})

    # Create sample routes
    routes = [
        ("JFK", "LHR"),
        ("LHR", "JFK"),
        ("JFK", "DXB"),
        ("DXB", "JFK"),
        ("LHR", "DXB")
    ]

    # Generate 90 days of booking data
    for i in range(90):
        date = datetime.now() - timedelta(days=90 - i)

        # Create 5-20 bookings per day
        for _ in range(random.randint(5, 20)):
            route = random.choice(routes)
            seat_class = random.choice(["Economy", "Premium Economy", "Business", "First Class"])
            price_multiplier = {
                "Economy": 1.0,
                "Premium Economy": 1.3,
                "Business": 1.8,
                "First Class": 2.5
            }[seat_class]
            base_price = random.choice([400, 450, 500, 550, 600])

            db.bookings.insert_one({
                "flight_number": f"SK{random.randint(100, 999)}",
                "route": f"{route[0]}-{route[1]}",
                "price": round(base_price * price_multiplier, 2),
                "seat_class": seat_class,
                "passenger_email": f"passenger{random.randint(1, 1000)}@example.com",
                "timestamp": date
            })

    print("Created sample analytics data with 90 days of booking history")
    client.close()