import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class BookingDialog(tk.Toplevel):  # Changed from ttk.Toplevel to tk.Toplevel
    def __init__(self, parent, session, flight_number, callback):
        super().__init__(parent)
        self.session = session
        self.flight_number = flight_number
        self.callback = callback

        self.title(f"Book Flight {flight_number}")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Flight info
        ttk.Label(main_frame, text=f"Booking Flight: {self.flight_number}",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

        # Passenger details
        ttk.Label(main_frame, text="Passenger Details",
                  font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=5)

        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Passport Number", "passport_number")
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields, start=2):
            ttk.Label(main_frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(main_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.entries[field] = entry

        # Seat class
        ttk.Label(main_frame, text="Seat Class:").grid(row=len(fields) + 2, column=0, sticky="w")
        self.seat_class = ttk.Combobox(main_frame, values=["Economy", "Premium Economy", "Business", "First Class"])
        self.seat_class.grid(row=len(fields) + 2, column=1, sticky="ew", padx=5)
        self.seat_class.current(0)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Confirm Booking", command=self.confirm_booking).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def confirm_booking(self):
        from database.models import Booking, Passenger, Flight

        try:
            # Get flight
            flight = self.session.query(Flight).filter(
                Flight.flight_number == self.flight_number
            ).first()

            if not flight:
                messagebox.showerror("Error", "Flight not found")
                return



            # Create passenger
            passenger = Passenger(
                first_name=self.entries['first_name'].get(),
                last_name=self.entries['last_name'].get(),
                email=self.entries['email'].get(),
                phone=self.entries['phone'].get(),
                passport_number=self.entries['passport_number'].get()
            )
            self.session.add(passenger)
            self.session.flush()

            # Create booking
            booking = Booking(
                flight_id=flight.id,
                passenger_id=passenger.id,
                booking_date=datetime.now(),
                seat_class=self.seat_class.get(),
                status="Confirmed"
            )
            self.session.add(booking)
            self.session.commit()

            messagebox.showinfo("Success", f"Booking confirmed!\nReference: {booking.id}")
            self.callback()
            self.destroy()

            messagebox.showinfo("Success", f"Booking confirmed!\nReference: {booking.id}")
            self.callback()  # This refreshes the bookings list
            self.destroy()


        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Booking failed: {str(e)}")