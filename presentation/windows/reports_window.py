# presentation/windows/reports_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from database.models import Booking, Flight, Airport
from config import settings
from pymongo import MongoClient
from presentation.plotly_chart import PlotlyChart



import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportsWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()

        # MongoDB connection
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client["skylink_analytics"]

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Analytics Dashboard", style="Title.TLabel").pack(pady=10)

        # Notebook for different reports
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)

        # Create tabs
        self.create_booking_trends_tab()
        self.create_route_analysis_tab()
        self.create_flight_occupancy_tab()

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(pady=10)

    def create_booking_trends_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Booking Trends")

        # Controls frame
        controls = ttk.Frame(tab)
        controls.pack(pady=10)

        ttk.Label(controls, text="Time Period:").pack(side="left")
        self.period = ttk.Combobox(
            controls,
            values=["7 days", "14 days", "30 days", "90 days"],
            state="readonly"
        )
        self.period.pack(side="left", padx=5)
        self.period.current(2)  # Default to 30 days

        ttk.Button(
            controls,
            text="Generate",
            command=lambda: self.update_booking_trends(tab),
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Chart frame
        self.trend_chart_frame = ttk.Frame(tab)
        self.trend_chart_frame.pack(fill="both", expand=True)

        # Initial load
        self.update_booking_trends(tab)

    def update_booking_trends(self, tab):
        # Clear previous chart
        for widget in self.trend_chart_frame.winfo_children():
            widget.destroy()

        try:
            days = int(self.period.get().split()[0])
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Try MongoDB first
            try:
                pipeline = [
                    {
                        "$match": {
                            "timestamp": {"$gte": start_date, "$lte": end_date}
                        }
                    },
                    {
                        "$group": {
                            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                            "count": {"$sum": 1},
                            "total": {"$sum": "$price"}
                        }
                    },
                    {"$sort": {"_id": 1}}
                ]

                data = list(self.db.bookings.aggregate(pipeline))
                use_mongodb = True
            except:
                # Fallback to SQLite
                bookings = self.session.query(Booking) \
                    .filter(Booking.booking_date >= start_date) \
                    .all()

                # Process SQLite data into similar format
                from collections import defaultdict
                daily_data = defaultdict(lambda: {"count": 0, "total": 0.0})
                for booking in bookings:
                    date_str = booking.booking_date.strftime("%Y-%m-%d")
                    daily_data[date_str]["count"] += 1
                    daily_data[date_str]["total"] += booking.final_price or booking.flight.base_price

                data = [{"_id": k, "count": v["count"], "total": v["total"]}
                        for k, v in daily_data.items()]
                data.sort(key=lambda x: x["_id"])
                use_mongodb = False

            if not data:
                ttk.Label(self.trend_chart_frame, text="No data available").pack()
                return

            dates = [item["_id"] for item in data]
            counts = [item["count"] for item in data]
            revenue = [item["total"] for item in data]

            # Create Plotly figure
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=counts,
                    name="Bookings",
                    marker_color='#4682B4'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=revenue,
                    name="Revenue",
                    line=dict(color='#5F9EA0', width=3)
                ),
                secondary_y=True
            )

            fig.update_layout(
                title=f"Booking Trends - Last {days} Days ({'MongoDB' if use_mongodb else 'SQLite'})",
                xaxis_title="Date",
                yaxis_title="Number of Bookings",
                yaxis2_title="Revenue ($)",
                template="plotly_white",
                height=500
            )

            # Display in Tkinter
            chart = PlotlyChart(self.trend_chart_frame, fig)
            chart.pack(fill="both", expand=True)

        except Exception as e:
            ttk.Label(self.trend_chart_frame, text=f"Error: {str(e)}").pack()

    def create_route_analysis_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Route Analysis")

        # Chart frame
        self.route_chart_frame = ttk.Frame(tab)
        self.route_chart_frame.pack(fill="both", expand=True)

        # Initial load
        self.update_route_analysis(tab)

    def update_route_analysis(self, tab):
        for widget in self.route_chart_frame.winfo_children():
            widget.destroy()

        try:
            # Try MongoDB first
            try:
                pipeline = [
                    {"$group": {
                        "_id": "$route",
                        "count": {"$sum": 1},
                        "avg_price": {"$avg": "$price"}
                    }},
                    {"$sort": {"count": -1}},
                    {"$limit": 10}
                ]
                data = list(self.db.bookings.aggregate(pipeline))
                use_mongodb = True
            except:
                # Fallback to SQLite
                from sqlalchemy import func
                routes = self.session.query(
                    Flight.departure_airport_code,
                    Flight.arrival_airport_code,
                    func.count(Booking.id),
                    func.avg(Booking.final_price)
                ).join(Booking) \
                    .group_by(Flight.departure_airport_code, Flight.arrival_airport_code) \
                    .order_by(func.count(Booking.id).desc()) \
                    .limit(10) \
                    .all()

                data = [{
                    "_id": f"{dep}-{arr}",
                    "count": count,
                    "avg_price": float(avg_price or 0)
                } for dep, arr, count, avg_price in routes]
                use_mongodb = False

            if not data:
                ttk.Label(self.route_chart_frame, text="No route data available").pack()
                return

            routes = [item["_id"] for item in data]
            counts = [item["count"] for item in data]
            avg_prices = [item["avg_price"] for item in data]

            # Create Plotly figure
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Bar(
                    x=routes,
                    y=counts,
                    name="Number of Bookings",
                    marker_color='#4682B4'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(
                    x=routes,
                    y=avg_prices,
                    name="Average Price",
                    line=dict(color='#5F9EA0', width=3)
                ),
                secondary_y=True
            )

            fig.update_layout(
                title=f"Top 10 Popular Routes ({'MongoDB' if use_mongodb else 'SQLite'})",
                xaxis_title="Route",
                yaxis_title="Number of Bookings",
                yaxis2_title="Average Price ($)",
                template="plotly_white",
                height=500
            )

            # Display in Tkinter
            chart = PlotlyChart(self.route_chart_frame, fig)
            chart.pack(fill="both", expand=True)

        except Exception as e:
            ttk.Label(self.route_chart_frame, text=f"Error: {str(e)}").pack()

    def create_flight_occupancy_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Flight Occupancy")

        # Chart frame
        self.occupancy_chart_frame = ttk.Frame(tab)
        self.occupancy_chart_frame.pack(fill="both", expand=True)

        # Initial load
        self.update_flight_occupancy(tab)

    def update_flight_occupancy(self, tab):
        for widget in self.occupancy_chart_frame.winfo_children():
            widget.destroy()

        try:
            flights = self.session.query(Flight) \
                .order_by(Flight.departure_time.desc()) \
                .limit(10) \
                .all()

            if not flights:
                ttk.Label(self.occupancy_chart_frame, text="No flight data available").pack()
                return

            flight_nums = []
            capacities = []
            bookings = []
            occupancy_rates = []

            for flight in flights:
                flight_nums.append(flight.flight_number)
                capacities.append(flight.aircraft.capacity)
                bookings.append(len(flight.bookings))
                occupancy_rates.append((len(flight.bookings) / flight.aircraft.capacity) * 100)

            # Create Plotly figure
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Bar(
                    x=flight_nums,
                    y=capacities,
                    name="Capacity",
                    marker_color='#D3D3D3'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Bar(
                    x=flight_nums,
                    y=bookings,
                    name="Booked",
                    marker_color='#4682B4'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(
                    x=flight_nums,
                    y=occupancy_rates,
                    name="Occupancy Rate",
                    line=dict(color='#FFA500', width=3)
                ),
                secondary_y=True
            )

            fig.update_layout(
                title="Flight Occupancy (Last 10 Flights)",
                xaxis_title="Flight Number",
                yaxis_title="Number of Seats",
                yaxis2_title="Occupancy Rate (%)",
                template="plotly_white",
                barmode='overlay',
                height=500
            )

            # Display in Tkinter
            chart = PlotlyChart(self.occupancy_chart_frame, fig)
            chart.pack(fill="both", expand=True)

        except Exception as e:
            ttk.Label(self.occupancy_chart_frame, text=f"Error: {str(e)}").pack()

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()