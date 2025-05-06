import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Flight, FlightStatus, Airport, Aircraft
from datetime import datetime, timedelta
from presentation.widgets.date_picker import DatePicker


class FlightDialog(tk.Toplevel):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback
        self.title("Add New Flight")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Get available airports and aircraft for dropdowns
        airports = [airport.code for airport in self.session.query(Airport).order_by(Airport.code).all()]
        aircrafts = [(ac.id, f"{ac.model} (Capacity: {ac.capacity})")
                    for ac in self.session.query(Aircraft).order_by(Aircraft.model).all()]

        # Flight number
        ttk.Label(main_frame, text="Flight Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flight_number = ttk.Entry(main_frame)
        self.flight_number.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Departure airport (Combobox)
        ttk.Label(main_frame, text="Departure Airport:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.departure_airport = ttk.Combobox(main_frame, values=airports, state="readonly")
        self.departure_airport.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        if airports:
            self.departure_airport.current(0)

        # Arrival airport (Combobox)
        ttk.Label(main_frame, text="Arrival Airport:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.arrival_airport = ttk.Combobox(main_frame, values=airports, state="readonly")
        self.arrival_airport.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        if len(airports) > 1:
            self.arrival_airport.current(1)

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

        # Flight duration (hours)
        ttk.Label(main_frame, text="Flight Duration (hours):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.flight_duration = ttk.Spinbox(main_frame, from_=1, to=24, increment=0.5)
        self.flight_duration.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        self.flight_duration.set("7.0")

        # Aircraft selection (Combobox)
        ttk.Label(main_frame, text="Aircraft:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.aircraft = ttk.Combobox(main_frame, state="readonly")
        self.aircraft.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)
        if aircrafts:
            self.aircraft['values'] = [ac[1] for ac in aircrafts]
            self.aircraft.current(0)
            self.aircraft_ids = [ac[0] for ac in aircrafts]  # Store mapping to actual IDs

        # Base price
        ttk.Label(main_frame, text="Base Price:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.base_price = ttk.Entry(main_frame)
        self.base_price.grid(row=7, column=1, sticky=tk.EW, padx=5, pady=5)
        self.base_price.insert(0, "100.00")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def save_flight(self):
        try:
            # Validate inputs
            if not self.flight_number.get():
                messagebox.showerror("Error", "Flight number is required")
                return

            if not self.departure_airport.get() or not self.arrival_airport.get():
                messagebox.showerror("Error", "Both departure and arrival airports are required")
                return

            if self.departure_airport.get() == self.arrival_airport.get():
                messagebox.showerror("Error", "Departure and arrival airports cannot be the same")
                return

            # Combine date and time
            departure_datetime = datetime.strptime(
                f"{self.departure_time.get_date()} {self.time_entry.get()}",
                "%Y-%m-%d %H:%M"
            )

            # Calculate arrival time
            try:
                duration = float(self.flight_duration.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid flight duration")
                return

            arrival_datetime = departure_datetime + timedelta(hours=duration)

            # Check if flight number exists
            existing = self.session.query(Flight) \
                .filter(Flight.flight_number == self.flight_number.get()) \
                .first()
            if existing:
                messagebox.showerror("Error", "Flight number already exists")
                return

            # Get selected aircraft ID
            if not hasattr(self, 'aircraft_ids') or not self.aircraft_ids:
                messagebox.showerror("Error", "No aircraft available")
                return

            selected_aircraft_index = self.aircraft.current()
            aircraft_id = self.aircraft_ids[selected_aircraft_index]

            # Create flight
            flight = Flight(
                flight_number=self.flight_number.get(),
                departure_airport_code=self.departure_airport.get(),
                arrival_airport_code=self.arrival_airport.get(),
                departure_time=departure_datetime,
                arrival_time=arrival_datetime,
                aircraft_id=aircraft_id,
                base_price=float(self.base_price.get()),
                status=FlightStatus.SCHEDULED
            )

            self.session.add(flight)
            self.session.commit()
            self.callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Failed to save flight: {str(e)}")