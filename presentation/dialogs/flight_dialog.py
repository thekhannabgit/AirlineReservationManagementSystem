import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Flight
from datetime import datetime


class FlightDialog(tk.Toplevel):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback
        self.title("Add New Flight")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Flight number
        ttk.Label(main_frame, text="Flight Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flight_number = ttk.Entry(main_frame)
        self.flight_number.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Departure airport
        ttk.Label(main_frame, text="Departure Airport:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.departure_airport = ttk.Entry(main_frame)
        self.departure_airport.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # Arrival airport
        ttk.Label(main_frame, text="Arrival Airport:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.arrival_airport = ttk.Entry(main_frame)
        self.arrival_airport.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # Departure time
        ttk.Label(main_frame, text="Departure Time:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.departure_time = ttk.Entry(main_frame)
        self.departure_time.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        self.departure_time.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def save_flight(self):
        try:
            flight = Flight(
                flight_number=self.flight_number.get(),
                departure_airport_code=self.departure_airport.get(),
                arrival_airport_code=self.arrival_airport.get(),
                departure_time=datetime.strptime(self.departure_time.get(), "%Y-%m-%d %H:%M"),
                arrival_time=datetime.strptime(self.departure_time.get(), "%Y-%m-%d %H:%M"),  # TODO: Calculate arrival
                aircraft_id=1,  # TODO: Select aircraft
                base_price=100.00  # TODO: Set proper price
            )
            self.session.add(flight)
            self.session.commit()
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flight: {str(e)}")