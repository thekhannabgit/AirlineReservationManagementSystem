import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.models import Booking, Passenger, Flight

class BookingDialog(tk.Toplevel):
    def __init__(self, parent, session, flight_number, callback):
        super().__init__(parent)
        self.session = session
        self.flight_number = flight_number
        self.callback = callback
        self.controller = parent.controller  # Needed for current_user

        self.title(f"Book Flight {flight_number}")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text=f"Booking Flight: {self.flight_number}",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

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

        # Auto-fill email if user is logged in
        if self.controller.current_user:
            self.entries["email"].insert(0, self.controller.current_user.email)

        ttk.Label(main_frame, text="Seat Class:").grid(row=len(fields) + 2, column=0, sticky="w")
        self.seat_class = ttk.Combobox(main_frame, values=["Economy", "Premium Economy", "Business", "First Class"])
        self.seat_class.grid(row=len(fields) + 2, column=1, sticky="ew", padx=5)
        self.seat_class.current(0)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Confirm Booking", command=self.confirm_booking).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

        main_frame.columnconfigure(1, weight=1)

    def confirm_booking(self):
        try:
            flight = self.session.query(Flight).filter(
                Flight.flight_number == self.flight_number
            ).first()

            if not flight:
                messagebox.showerror("Error", "Flight not found")
                return

            email = self.entries['email'].get()
            passenger = self.session.query(Passenger).filter(Passenger.email == email).first()

            if not passenger:
                # Create new passenger only if not found
                passenger = Passenger(
                    first_name=self.entries['first_name'].get(),
                    last_name=self.entries['last_name'].get(),
                    email=email,
                    phone=self.entries['phone'].get(),
                    passport_number=self.entries['passport_number'].get()
                )
                self.session.add(passenger)
                self.session.flush()

            booking = Booking(
                flight_id=flight.id,
                passenger_id=passenger.id,
                booking_date=datetime.now(),
                seat_class=self.seat_class.get(),
                status="Confirmed",
                final_price=flight.base_price  # Optional: can apply multiplier logic if needed
            )

            self.session.add(booking)
            self.session.commit()

            messagebox.showinfo("Success", f"Booking confirmed!\nReference: {booking.id}")
            self.callback()
            self.destroy()

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Booking failed: {str(e)}")
