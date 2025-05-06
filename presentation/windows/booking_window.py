# presentation/windows/booking_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.models import Flight, Airport, Booking, Passenger, FlightStatus


class BookingWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()
        self.load_flights()
        self.load_my_bookings()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Available Flights tab
        flights_frame = ttk.Frame(self.notebook)
        self.create_flights_tab(flights_frame)
        self.notebook.add(flights_frame, text="Available Flights")

        # My Bookings tab
        bookings_frame = ttk.Frame(self.notebook)
        self.create_bookings_tab(bookings_frame)
        self.notebook.add(bookings_frame, text="My Bookings")

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(pady=10)

    def create_flights_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Available Flights",
                  style="Subtitle.TLabel").pack(pady=10)

        # Treeview with selection style
        style = ttk.Style()
        style.map('Treeview', background=[('selected', '#347083')])  # Blue selection color

        # Treeview
        self.flight_tree = ttk.Treeview(
            frame,
            columns=("flight", "departure", "arrival", "time", "status", "price"),
            show="headings",
            height=10
        )

        # Configure columns
        columns = [
            ("flight", "Flight #", 100),
            ("departure", "From", 150),
            ("arrival", "To", 150),
            ("time", "Departure", 150),
            ("status", "Status", 100),
            ("price", "Price ($)", 100)
        ]

        for col_id, heading, width in columns:
            self.flight_tree.heading(col_id, text=heading)
            self.flight_tree.column(col_id, width=width, anchor=tk.CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                  command=self.flight_tree.yview)
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.flight_tree.pack(side="left", fill="both", expand=True, pady=10)

        # Book button
        ttk.Button(
            frame,
            text="Book Selected Flight",
            command=self.book_flight,
            style="Accent.TButton"
        ).pack(pady=10)

    def create_bookings_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="My Bookings",
                  style="Subtitle.TLabel").pack(pady=10)

        # Treeview
        self.bookings_tree = ttk.Treeview(
            frame,
            columns=("id", "flight", "date", "status", "class", "price"),
            show="headings",
            height=10
        )

        # Configure columns
        columns = [
            ("id", "Booking ID", 80),
            ("flight", "Flight", 120),
            ("date", "Booking Date", 150),
            ("status", "Status", 100),
            ("class", "Class", 100),
            ("price", "Price ($)", 100)
        ]

        for col_id, heading, width in columns:
            self.bookings_tree.heading(col_id, text=heading)
            self.bookings_tree.column(col_id, width=width, anchor=tk.CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                  command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.bookings_tree.pack(side="left", fill="both", expand=True, pady=10)

        # Button frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Cancel Booking",
            command=self.cancel_booking,
            style="Warning.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_my_bookings
        ).pack(side="left", padx=5)

    def load_flights(self):
        """Load available flights into the treeview"""
        self.flight_tree.delete(*self.flight_tree.get_children())

        try:
            # Get current datetime for filtering future flights
            now = datetime.now()

            flights = self.session.query(Flight) \
                .join(Airport, Flight.departure_airport_code == Airport.code) \
                .filter(
                Flight.status == FlightStatus.SCHEDULED
,
                Flight.departure_time > now
            ) \
                .order_by(Flight.departure_time.asc()) \
                .all()

            for flight in flights:
                # Get arrival airport details
                arrival_airport = self.session.query(Airport) \
                    .filter(Airport.code == flight.arrival_airport_code) \
                    .first()

                self.flight_tree.insert("", "end", values=(
                    flight.flight_number,
                    f"{flight.departure_airport.code} ({flight.departure_airport.city})",
                    f"{arrival_airport.code} ({arrival_airport.city})",
                    flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                    flight.status,
                    f"{flight.base_price:.2f}"
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flights: {str(e)}")

    '''def load_my_bookings(self):
        self.bookings_tree.delete(*self.bookings_tree.get_children())

        if not self.controller.current_user:
            return

        try:
            # Find or create passenger for current user
            passenger = self.session.query(Passenger) \
                .filter(Passenger.email == self.controller.current_user.email) \
                .first()

            if not passenger:
                # Create new passenger record if none exists
                passenger = Passenger(
                    first_name=self.controller.current_user.username,
                    last_name="",
                    email=self.controller.current_user.email,
                    phone="",
                    passport_number=""
                )
                self.session.add(passenger)
                self.session.commit()

            bookings = self.session.query(Booking) \
                .join(Flight) \
                .filter(Booking.passenger_id == passenger.id) \
                .order_by(Booking.booking_date.desc()) \
                .all()

            for booking in bookings:
                self.bookings_tree.insert("", "end", values=(
                    booking.id,
                    booking.flight.flight_number,
                    booking.booking_date.strftime("%Y-%m-%d %H:%M"),
                    booking.status,
                    booking.seat_class,
                    f"{(booking.final_price or booking.flight.base_price):.2f}"
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")'''

    def load_my_bookings(self):
        """Load current user's bookings"""
        self.bookings_tree.delete(*self.bookings_tree.get_children())

        if not self.controller.current_user:
            return

        try:
            # Get or create passenger record for current user
            passenger = self.session.query(Passenger) \
                .filter(Passenger.email == self.controller.current_user.email) \
                .first()

            if not passenger:
                # Create new passenger if doesn't exist
                passenger = Passenger(
                    first_name=self.controller.current_user.username,
                    last_name="",
                    email=self.controller.current_user.email,
                    phone="",
                    passport_number=""
                )
                self.session.add(passenger)
                self.session.commit()

            # Get all bookings for this passenger
            bookings = self.session.query(Booking) \
                .join(Flight) \
                .filter(Booking.passenger_id == passenger.id) \
                .order_by(Booking.booking_date.desc()) \
                .all()

            for booking in bookings:
                self.bookings_tree.insert("", "end", values=(
                    booking.id,
                    booking.flight.flight_number,
                    booking.booking_date.strftime("%Y-%m-%d %H:%M"),
                    booking.status,
                    booking.seat_class,
                    f"{(booking.final_price or booking.flight.base_price):.2f}"
                ))

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
            print(f"Error loading bookings: {e}")

    def book_flight(self):
        selected = self.flight_tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Please select a flight first")
            return

        flight_data = self.flight_tree.item(selected)['values']
        from presentation.dialogs.booking_dialog import BookingDialog
        BookingDialog(
            self,
            self.session,
            flight_data[0],  # flight number
            callback=self.load_my_bookings
        )

    def cancel_booking(self):
        selected = self.bookings_tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Please select a booking to cancel")
            return

        booking_id = self.bookings_tree.item(selected)['values'][0]

        try:
            booking = self.session.query(Booking).get(booking_id)
            if booking:
                booking.status = "Cancelled"
                self.session.commit()
                messagebox.showinfo("Success", "Booking cancelled")
                self.load_my_bookings()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")