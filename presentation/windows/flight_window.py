import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Flight


class FlightWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.load_flights()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for flights
        self.tree = ttk.Treeview(main_frame, columns=("flight_no", "departure", "arrival", "time", "status"),
                                 show="headings")
        self.tree.heading("flight_no", text="Flight #")
        self.tree.heading("departure", text="From")
        self.tree.heading("arrival", text="To")
        self.tree.heading("time", text="Departure Time")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Add Flight", command=self.add_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_flights).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=self.go_back).pack(side=tk.RIGHT, padx=5)

    def load_flights(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load flights from database
        flights = self.controller.session.query(Flight).order_by(Flight.departure_time).all()
        for flight in flights:
            self.tree.insert("", tk.END, values=(
                flight.flight_number,
                flight.departure_airport_code,
                flight.arrival_airport_code,
                flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                flight.status.value
            ))

    def add_flight(self):
        from ..dialogs.flight_dialog import FlightDialog
        FlightDialog(self, self.controller.session, self.load_flights)

    def go_back(self):
        from .dashboard import Dashboard
        dashboard = Dashboard(self.master, self.controller)
        dashboard.grid(row=0, column=0, sticky="nsew")
        dashboard.tkraise()