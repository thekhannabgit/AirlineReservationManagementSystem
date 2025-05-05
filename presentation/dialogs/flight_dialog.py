# presentation/dialogs/flight_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Flight
from datetime import datetime, timedelta
from presentation.widgets.date_picker import DatePicker


class FlightDialog(tk.Toplevel):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback
        self.title("Add New Flight")
        self.geometry("500x400")
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
        self.departure_time = DatePicker(main_frame)
        self.departure_time.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        self.departure_time.set_date(datetime.now().strftime("%Y-%m-%d"))

        # Time entry
        ttk.Label(main_frame, text="Time (HH:MM):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(main_frame)
        self.time_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        self.time_entry.insert(0, datetime.now().strftime("%H:%M"))

        # Base price
        ttk.Label(main_frame, text="Base Price:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.base_price = ttk.Entry(main_frame)
        self.base_price.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        self.base_price.insert(0, "100.00")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def save_flight(self):
        try:
            # Combine date and time
            departure_datetime = datetime.strptime(
                f"{self.departure_time.get_date()} {self.time_entry.get()}",
                "%Y-%m-%d %H:%M"
            )

            flight = Flight(
                flight_number=self.flight_number.get(),
                departure_airport_code=self.departure_airport.get(),
                arrival_airport_code=self.arrival_airport.get(),
                departure_time=departure_datetime,
                arrival_time=departure_datetime + timedelta(hours=2),  # Default 2-hour flight
                aircraft_id=1,  # TODO: Add aircraft selection
                base_price=float(self.base_price.get())
            )

            self.session.add(flight)
            self.session.commit()
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flight: {str(e)}")