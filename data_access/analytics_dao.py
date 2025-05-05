# data_access/analytics_dao.py (updated)
from datetime import datetime, timedelta
from typing import Dict, List

from pymongo import MongoClient

from config import settings


class AnalyticsDAO:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client["skylink_analytics"]

    def log_booking(self, booking_data: Dict):
        self.db.bookings.insert_one({
            **booking_data,
            "timestamp": datetime.now()
        })

    def get_booking_trends(self, days: int) -> List[Dict]:
        pipeline = [
            {
                "$match": {
                    "timestamp": {
                        "$gte": datetime.now() - timedelta(days=days)
                    }
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "count": {"$sum": 1},
                    "total_revenue": {"$sum": "$price"}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        return list(self.db.bookings.aggregate(pipeline))

    def get_popular_routes(self, limit: int = 5) -> List[Dict]:
        pipeline = [
            {"$group": {
                "_id": "$route",
                "count": {"$sum": 1},
                "average_price": {"$avg": "$price"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        return list(self.db.bookings.aggregate(pipeline))