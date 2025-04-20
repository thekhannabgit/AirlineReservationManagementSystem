import tkinter as tk
from tkinter import ttk, messagebox


class BookingDialog(tk.Toplevel):
    def __init__(self, parent, session, flight_id, callback):
        super().__init__(parent)
        self.session = session
        self.flight_id = flight_id
        self.callback = callback
        self.title("New Booking")
        self.create_widgets()

    def create_widgets(self):
        # Form fields
        ttk.Label(self, text="Passenger Details").pack(pady=5)

        # Entry fields for passenger info
        # Submit button
        ttk.Button(self, text="Confirm Booking", command=self.create_booking).pack(pady=10)

    def create_booking(self):
        # Implementation here
        pass