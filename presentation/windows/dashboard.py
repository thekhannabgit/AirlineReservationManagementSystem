import tkinter as tk
from tkinter import ttk


class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True)

        # Title
        ttk.Label(main_frame, text="Dashboard", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons
        buttons = [
            ("Flight Management", self.open_flight_window),
            ("Booking Management", self.open_booking_window),
            ("Crew Management", self.open_crew_window),
            ("Reports", self.open_reports_window)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(main_frame, text=text, command=command).grid(row=i, column=0, pady=5, sticky=tk.EW)

    def open_flight_window(self):
        from .flight_window import FlightWindow
        flight_window = FlightWindow(self.master, self.controller)
        flight_window.grid(row=0, column=0, sticky="nsew")
        flight_window.tkraise()

    def open_booking_window(self):
        from .booking_window import BookingWindow
        booking_window = BookingWindow(self.master, self.controller)
        booking_window.grid(row=0, column=0, sticky="nsew")
        booking_window.tkraise()

    def open_crew_window(self):
        from .crew_window import CrewWindow
        crew_window = CrewWindow(self.master, self.controller)
        crew_window.grid(row=0, column=0, sticky="nsew")
        crew_window.tkraise()

    def open_reports_window(self):
        from .reports_window import ReportsWindow
        reports_window = ReportsWindow(self.master, self.controller)
        reports_window.grid(row=0, column=0, sticky="nsew")
        reports_window.tkraise()