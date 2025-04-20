from data_access.analytics_dao import AnalyticsDAO
from typing import List, Dict


class ReportingService:
    def __init__(self, session=None):
        self.analytics_dao = AnalyticsDAO()

    def get_booking_trends(self, days: int = 30) -> List[Dict]:
        return self.analytics_dao.get_booking_trends(days)

    def get_popular_routes(self, limit: int = 5) -> List[Dict]:
        return self.analytics_dao.get_popular_routes(limit)