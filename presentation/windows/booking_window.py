# presentation/windows/booking_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from presentation.dialogs.booking_dialog import BookingDialog
from database.models import Flight, Airport, FlightStatus, Booking, Passenger
from tkinter import simpledialog

class BookingWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()
        self.load_flights()
        self.load_bookings()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Flights tab
        flights_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(flights_frame, text="Available Flights")

        # Bookings tab
        bookings_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(bookings_frame, text="My Bookings")

        # Available Flights Treeview
        ttk.Label(flights_frame, text="Available Flights", style="Subtitle.TLabel").pack(pady=10)

        tree_frame = ttk.Frame(flights_frame)
        tree_frame.pack(fill="both", expand=True)

        self.flight_tree = ttk.Treeview(
            tree_frame,
            columns=("flight", "departure", "arrival", "time", "status", "price"),
            show="headings",
            height=10
        )

        # Configure columns
        self.flight_tree.heading("flight", text="Flight #")
        self.flight_tree.heading("departure", text="From")
        self.flight_tree.heading("arrival", text="To")
        self.flight_tree.heading("time", text="Departure Time")
        self.flight_tree.heading("status", text="Status")
        self.flight_tree.heading("price", text="Price ($)")

        self.flight_tree.column("flight", width=100, anchor=tk.CENTER)
        self.flight_tree.column("departure", width=150, anchor=tk.W)
        self.flight_tree.column("arrival", width=150, anchor=tk.W)
        self.flight_tree.column("time", width=150, anchor=tk.CENTER)
        self.flight_tree.column("status", width=100, anchor=tk.CENTER)
        self.flight_tree.column("price", width=100, anchor=tk.CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.flight_tree.yview)
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.flight_tree.pack(side="left", fill="both", expand=True)

        # Book button
        btn_frame = ttk.Frame(flights_frame)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Book Selected Flight",
            command=self.book_flight,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_flights
        ).pack(side="left", padx=5)

        # My Bookings Treeview
        ttk.Label(bookings_frame, text="My Bookings", style="Subtitle.TLabel").pack(pady=10)

        bookings_tree_frame = ttk.Frame(bookings_frame)
        bookings_tree_frame.pack(fill="both", expand=True)

        self.bookings_tree = ttk.Treeview(
            bookings_tree_frame,
            columns=("id", "flight", "date", "class", "status", "price"),
            show="headings",
            height=10
        )

        # Configure columns
        self.bookings_tree.heading("id", text="Booking ID")
        self.bookings_tree.heading("flight", text="Flight #")
        self.bookings_tree.heading("date", text="Booking Date")
        self.bookings_tree.heading("class", text="Class")
        self.bookings_tree.heading("status", text="Status")
        self.bookings_tree.heading("price", text="Price ($)")

        self.bookings_tree.column("id", width=80, anchor=tk.CENTER)
        self.bookings_tree.column("flight", width=100, anchor=tk.CENTER)
        self.bookings_tree.column("date", width=150, anchor=tk.CENTER)
        self.bookings_tree.column("class", width=120, anchor=tk.CENTER)
        self.bookings_tree.column("status", width=100, anchor=tk.CENTER)
        self.bookings_tree.column("price", width=100, anchor=tk.CENTER)

        # Add scrollbar
        bookings_scrollbar = ttk.Scrollbar(bookings_tree_frame, orient="vertical", command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=bookings_scrollbar.set)
        bookings_scrollbar.pack(side="right", fill="y")
        self.bookings_tree.pack(side="left", fill="both", expand=True)

        # Booking management buttons
        bookings_btn_frame = ttk.Frame(bookings_frame)
        bookings_btn_frame.pack(pady=10)

        ttk.Button(
            bookings_btn_frame,
            text="Cancel Booking",
            command=self.cancel_booking,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            bookings_btn_frame,
            text="Refresh",
            command=self.load_bookings
        ).pack(side="left", padx=5)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(pady=10)

    def load_flights(self):
        # Clear existing data
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)

        try:
            # Load flights with airport information
            flights = self.session.query(Flight) \
                .join(Airport, Flight.departure_airport_code == Airport.code) \
                .filter(Flight.status == FlightStatus.SCHEDULED) \
                .all()

            if not flights:
                messagebox.showinfo("Information", "No scheduled flights available")
                return

            for flight in flights:
                self.flight_tree.insert("", "end", values=(
                    flight.flight_number,
                    f"{flight.departure_airport.code} ({flight.departure_airport.city})",
                    f"{flight.arrival_airport.code} ({flight.arrival_airport.city})",
                    flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                    flight.status.value,
                    f"${flight.base_price:.2f}"
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flights: {str(e)}")

    def load_bookings(self):
        # Clear existing data
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)

        try:
            # For demo purposes, we'll show all bookings
            # In a real app, you'd filter by the logged-in user
            bookings = self.session.query(Booking) \
                .join(Flight) \
                .join(Passenger) \
                .order_by(Booking.booking_date.desc()) \
                .all()

            if not bookings:
                messagebox.showinfo("Information", "No bookings found")
                return

            for booking in bookings:
                self.bookings_tree.insert("", "end", values=(
                    booking.id,
                    booking.flight.flight_number,
                    booking.booking_date.strftime("%Y-%m-%d %H:%M"),
                    booking.seat_class,
                    booking.status,
                    f"${booking.final_price if booking.final_price else booking.flight.base_price:.2f}"
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")

    def book_flight(self):
        selected = self.flight_tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Please select a flight first")
            return

        flight_data = self.flight_tree.item(selected)['values']
        BookingDialog(
            self,
            self.session,
            flight_data[0],  # flight number
            flight_data[4],  # status
            float(flight_data[5][1:]),  # base price (remove $ and convert to float)
            callback=self.load_bookings
        )

    def cancel_booking(self):
        selected = self.bookings_tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Please select a booking first")
            return

        booking_data = self.bookings_tree.item(selected)['values']
        booking_id = booking_data[0]

        try:
            booking = self.session.query(Booking).filter(Booking.id == booking_id).first()
            if booking:
                booking.status = "Cancelled"
                self.session.commit()
                messagebox.showinfo("Success", "Booking cancelled successfully")
                self.load_bookings()
            else:
                messagebox.showerror("Error", "Booking not found")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")