# presentation/app.py
import tkinter as tk
from tkinter import ttk
from presentation.styles import configure_styles
from presentation.windows.auth_window import AuthWindow
from presentation.windows.dashboard import Dashboard
from presentation.windows.booking_window import BookingWindow
from presentation.windows.flight_window import FlightWindow
from presentation.windows.crew_window import CrewWindow
from presentation.windows.reports_window import ReportsWindow


class AirlineApp(tk.Tk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.current_user = None

        self.title("SkyLink Airways")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Configure styles
        configure_styles()

        # Container for all windows
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold window references
        self.windows = {}

        # Initialize all windows
        self.init_windows()

        # Show auth window first
        self.show_window('AuthWindow')

    def init_windows(self):
        windows = {
            'AuthWindow': AuthWindow,
            'Dashboard': Dashboard,
            'BookingWindow': BookingWindow,
            'FlightWindow': FlightWindow,
            'CrewWindow': CrewWindow,
            'ReportsWindow': ReportsWindow
        }

        for name, WindowClass in windows.items():
            window = WindowClass(self.container, self)
            self.windows[name] = window
            window.grid(row=0, column=0, sticky="nsew")

    def show_window(self, window_name):
        window = self.windows[window_name]
        window.tkraise()

        # Call on_show method if it exists
        if hasattr(window, 'on_show'):
            window.on_show()

        # Update window title with current user info
        if self.current_user:
            title = f"SkyLink Airways - {self.current_user.username}"
            if hasattr(self.current_user, 'role'):
                title += f" ({self.current_user.role.value})"
            self.title(title)
        else:
            self.title("SkyLink Airways")

    def logout(self):
        self.current_user = None
        self.show_window('AuthWindow')