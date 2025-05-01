# presentation/windows/reports_window.py
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import settings
from pymongo import MongoClient


class ReportsWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()

        # MongoDB connection
        self.mongo_client = MongoClient(settings.MONGODB_URI)
        self.analytics_db = self.mongo_client["skylink_analytics"]

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Analytics Reports", style="Title.TLabel").pack(pady=10)

        # Notebook for different reports
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)

        # Booking Trends tab
        trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(trends_frame, text="Booking Trends")

        # Popular Routes tab
        routes_frame = ttk.Frame(self.notebook)
        self.notebook.add(routes_frame, text="Popular Routes")

        # Flight Occupancy tab
        occupancy_frame = ttk.Frame(self.notebook)
        self.notebook.add(occupancy_frame, text="Flight Occupancy")

        # Revenue tab
        revenue_frame = ttk.Frame(self.notebook)
        self.notebook.add(revenue_frame, text="Revenue Analysis")

        # Setup each tab
        self.setup_trends_tab(trends_frame)
        self.setup_routes_tab(routes_frame)
        self.setup_occupancy_tab(occupancy_frame)
        self.setup_revenue_tab(revenue_frame)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(pady=10)

    def setup_trends_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        # Days selection
        days_frame = ttk.Frame(frame)
        days_frame.pack(pady=10)

        ttk.Label(days_frame, text="Days to analyze:").pack(side="left")
        self.trend_days = ttk.Combobox(days_frame, values=[7, 14, 30, 60, 90], state="readonly")
        self.trend_days.pack(side="left", padx=5)
        self.trend_days.current(2)  # Default to 30 days

        ttk.Button(
            days_frame,
            text="Generate Report",
            command=self.generate_trends_report,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Chart frame
        self.trend_chart_frame = ttk.Frame(frame)
        self.trend_chart_frame.pack(fill="both", expand=True)

    def setup_routes_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        # Limit selection
        limit_frame = ttk.Frame(frame)
        limit_frame.pack(pady=10)

        ttk.Label(limit_frame, text="Top routes to show:").pack(side="left")
        self.route_limit = ttk.Combobox(limit_frame, values=[5, 10, 15, 20], state="readonly")
        self.route_limit.pack(side="left", padx=5)
        self.route_limit.current(0)  # Default to 5

        ttk.Button(
            limit_frame,
            text="Generate Report",
            command=self.generate_routes_report,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Chart frame
        self.route_chart_frame = ttk.Frame(frame)
        self.route_chart_frame.pack(fill="both", expand=True)

    def setup_occupancy_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Flight Occupancy Report", style="Subtitle.TLabel").pack(pady=10)

        # Flight selection
        flight_frame = ttk.Frame(frame)
        flight_frame.pack(pady=10)

        ttk.Label(flight_frame, text="Select Flight:").pack(side="left")
        self.flight_selector = ttk.Combobox(flight_frame, state="readonly")
        self.flight_selector.pack(side="left", padx=5)
        self.load_flight_options()

        ttk.Button(
            flight_frame,
            text="Generate Report",
            command=self.generate_occupancy_report,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Chart frame
        self.occupancy_chart_frame = ttk.Frame(frame)
        self.occupancy_chart_frame.pack(fill="both", expand=True)

    def setup_revenue_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Revenue Analysis", style="Subtitle.TLabel").pack(pady=10)

        # Time period selection
        period_frame = ttk.Frame(frame)
        period_frame.pack(pady=10)

        ttk.Label(period_frame, text="Time Period:").pack(side="left")
        self.revenue_period = ttk.Combobox(period_frame,
                                           values=["Last 7 days", "Last 30 days", "Last 90 days", "Last year"],
                                           state="readonly")
        self.revenue_period.pack(side="left", padx=5)
        self.revenue_period.current(1)  # Default to 30 days

        ttk.Button(
            period_frame,
            text="Generate Report",
            command=self.generate_revenue_report,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Chart frame
        self.revenue_chart_frame = ttk.Frame(frame)
        self.revenue_chart_frame.pack(fill="both", expand=True)

    def load_flight_options(self):
        try:
            from database.models import Flight
            flights = self.session.query(Flight).order_by(Flight.flight_number).all()
            options = [f"{f.flight_number} ({f.departure_airport_code}-{f.arrival_airport_code})" for f in flights]
            self.flight_selector['values'] = options
            if options:
                self.flight_selector.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flight options: {str(e)}")

    def generate_trends_report(self):
        try:
            days = int(self.trend_days.get())

            # Get data from MongoDB
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

            results = list(self.analytics_db.bookings.aggregate(pipeline))

            if not results:
                messagebox.showinfo("Info", "No booking data available for the selected period")
                return

            # Prepare data for chart
            dates = [item["_id"] for item in results]
            counts = [item["count"] for item in results]
            revenues = [item["total_revenue"] for item in results]

            # Clear previous chart
            for widget in self.trend_chart_frame.winfo_children():
                widget.destroy()

            # Create figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

            # Bookings chart
            ax1.bar(dates, counts, color='#4682b4')
            ax1.set_title(f"Daily Bookings (Last {days} Days)")
            ax1.set_ylabel("Number of Bookings")
            ax1.tick_params(axis='x', rotation=45)

            # Revenue chart
            ax2.plot(dates, revenues, marker='o', color='#5f9ea0')
            ax2.set_title(f"Daily Revenue (Last {days} Days)")
            ax2.set_ylabel("Revenue ($)")
            ax2.tick_params(axis='x', rotation=45)

            plt.tight_layout()

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.trend_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate trends report: {str(e)}")

    def generate_routes_report(self):
        try:
            limit = int(self.route_limit.get())

            # Get data from MongoDB
            pipeline = [
                {"$group": {
                    "_id": {"route": "$route"},
                    "count": {"$sum": 1},
                    "average_price": {"$avg": "$price"}
                }},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]

            results = list(self.analytics_db.bookings.aggregate(pipeline))

            if not results:
                messagebox.showinfo("Info", "No route data available")
                return

            # Prepare data for chart
            routes = [item["_id"]["route"] for item in results]
            counts = [item["count"] for item in results]
            avg_prices = [item["average_price"] for item in results]

            # Clear previous chart
            for widget in self.route_chart_frame.winfo_children():
                widget.destroy()

            # Create figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

            # Popularity chart
            ax1.bar(routes, counts, color='#4682b4')
            ax1.set_title(f"Top {limit} Popular Routes")
            ax1.set_ylabel("Number of Bookings")
            ax1.tick_params(axis='x', rotation=45)

            # Price chart
            ax2.bar(routes, avg_prices, color='#5f9ea0')
            ax2.set_title(f"Average Prices by Route")
            ax2.set_ylabel("Average Price ($)")
            ax2.tick_params(axis='x', rotation=45)

            plt.tight_layout()

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.route_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate routes report: {str(e)}")

    def generate_occupancy_report(self):
        try:
            flight_str = self.flight_selector.get()
            if not flight_str:
                messagebox.showwarning("Warning", "Please select a flight first")
                return

            flight_number = flight_str.split(" ")[0]

            # Get flight details from SQLite
            from database.models import Flight, Booking
            flight = self.session.query(Flight).filter(Flight.flight_number == flight_number).first()

            if not flight:
                messagebox.showerror("Error", "Flight not found")
                return

            # Get bookings for this flight
            bookings = self.session.query(Booking).filter(Booking.flight_id == flight.id).count()

            # Calculate occupancy
            capacity = flight.aircraft.capacity
            occupancy_rate = (bookings / capacity) * 100

            # Clear previous chart
            for widget in self.occupancy_chart_frame.winfo_children():
                widget.destroy()

            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))

            # Occupancy chart
            labels = ['Occupied', 'Available']
            sizes = [bookings, capacity - bookings]
            colors = ['#4682b4', '#5f9ea0']

            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title(f"Occupancy for Flight {flight_number}\n({bookings}/{capacity} seats booked)")

            plt.tight_layout()

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.occupancy_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate occupancy report: {str(e)}")

    def generate_revenue_report(self):
        try:
            period = self.revenue_period.get()

            if period == "Last 7 days":
                days = 7
            elif period == "Last 30 days":
                days = 30
            elif period == "Last 90 days":
                days = 90
            else:  # Last year
                days = 365

            # Get data from MongoDB
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
                        "_id": {"$dateToString": {"format": "%Y-%m", "date": "$timestamp"}},
                        "total_revenue": {"$sum": "$price"}
                    }
                },
                {"$sort": {"_id": 1}}
            ]

            results = list(self.analytics_db.bookings.aggregate(pipeline))

            if not results:
                messagebox.showinfo("Info", "No revenue data available for the selected period")
                return

            # Prepare data for chart
            months = [item["_id"] for item in results]
            revenues = [item["total_revenue"] for item in results]

            # Clear previous chart
            for widget in self.revenue_chart_frame.winfo_children():
                widget.destroy()

            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))

            # Revenue chart
            ax.bar(months, revenues, color='#4682b4')
            ax.set_title(f"Monthly Revenue ({period})")
            ax.set_ylabel("Revenue ($)")
            ax.tick_params(axis='x', rotation=45)

            plt.tight_layout()

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.revenue_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate revenue report: {str(e)}")

    def __del__(self):
        # Close MongoDB connection when window is closed
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close()