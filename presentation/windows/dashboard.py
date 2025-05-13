import tkinter as tk
from tkinter import ttk, messagebox
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
        # Staff-only buttons
        elif self.controller.current_user.role == UserRole.STAFF:
            buttons.append(("Reports", self.open_reports_window))

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
        if self.controller.current_user.role in [UserRole.ADMIN, UserRole.STAFF]:
            self.controller.show_window('FlightWindow')
        else:
            messagebox.showwarning("Access Denied", "You don't have permission to access Flight Management")

    def open_booking_window(self):
        self.controller.show_window('BookingWindow')

    def open_crew_window(self):
        if self.controller.current_user.role == UserRole.ADMIN:
            self.controller.show_window('CrewWindow')
        else:
            messagebox.showwarning("Access Denied", "Only administrators can access Crew Management")

    def open_reports_window(self):
        if self.controller.current_user.role in [UserRole.ADMIN, UserRole.STAFF]:
            self.controller.show_window('ReportsWindow')
        else:
            messagebox.showwarning("Access Denied", "You don't have permission to access Reports")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_window('AuthWindow')