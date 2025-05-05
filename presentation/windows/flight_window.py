# presentation/windows/flight_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Flight, Aircraft, Airport

from datetime import datetime


class FlightWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()
        self.load_flights()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for flights
        self.tree = ttk.Treeview(main_frame, columns=(
            "flight_no", "departure", "arrival", "dep_time",
            "arr_time", "status", "price", "seats"
        ), show="headings")

        # Configure columns
        columns = [
            ("flight_no", "Flight #", 100),
            ("departure", "From", 150),
            ("arrival", "To", 150),
            ("dep_time", "Departure", 150),
            ("arr_time", "Arrival", 150),
            ("status", "Status", 100),
            ("price", "Price ($)", 80),
            ("seats", "Seats", 80)
        ]

        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            button_frame,
            text="Add Flight",
            command=self.add_flight,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_flights
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Back",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(side=tk.RIGHT, padx=5)

    def load_flights(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load flights from database
        flights = self.session.query(Flight) \
            .join(Aircraft) \
            .order_by(Flight.departure_time) \
            .all()

        for flight in flights:
            booked_seats = len(flight.bookings)
            available_seats = flight.aircraft.capacity - booked_seats

            self.tree.insert("", tk.END, values=(
                flight.flight_number,
                f"{flight.departure_airport_code} ({flight.departure_airport.city})",
                f"{flight.arrival_airport_code} ({flight.arrival_airport.city})",
                flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                flight.arrival_time.strftime("%Y-%m-%d %H:%M"),
                flight.status.value,
                f"{flight.base_price:.2f}",
                f"{booked_seats}/{flight.aircraft.capacity}"
            ))

    def add_flight(self):
        from ..dialogs.flight_dialog import FlightDialog
        FlightDialog(self, self.session, self.load_flights)