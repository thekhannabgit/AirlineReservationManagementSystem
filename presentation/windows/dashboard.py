# presentation/windows/dashboard.py
import tkinter as tk
from tkinter import ttk

from database.models import UserRole


class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        center_frame = ttk.Frame(main_frame)
        center_frame.pack(expand=True)

        ttk.Label(center_frame, text="SkyLink Dashboard",
                  style="Title.TLabel").pack(pady=20)

        # Common buttons for all users
        buttons = [
            ("Flight Management", self.open_flight_window),
            ("Booking Management", self.open_booking_window)
        ]

        # Admin-only buttons
        if self.controller.current_user.role == UserRole.ADMIN:
            buttons.extend([
                ("Crew Management", self.open_crew_window),
                ("Reports", self.open_reports_window)
            ])

        for text, command in buttons:
            btn = ttk.Button(
                center_frame,
                text=text,
                command=command,
                width=25,
                style="Accent.TButton"
            )
            btn.pack(pady=10, ipady=5)

        # Logout button
        ttk.Button(
            center_frame,
            text="Logout",
            command=self.logout,
            style="Warning.TButton"
        ).pack(pady=20)

    def open_flight_window(self):
        self.controller.show_window('FlightWindow')

    def open_booking_window(self):
        self.controller.show_window('BookingWindow')

    def open_crew_window(self):
        self.controller.show_window('CrewWindow')

    def open_reports_window(self):
        self.controller.show_window('ReportsWindow')

    def logout(self):
        self.controller.current_user = None
        self.controller.show_window('AuthWindow')