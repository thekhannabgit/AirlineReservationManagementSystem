import tkinter as tk
from tkinter import ttk
from presentation.styles import configure_styles


class AirlineApp(tk.Tk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.current_user = None

        self.title("SkyLink Airways")
        self.geometry("1200x800")
        configure_styles()

        # Container for all windows
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold window references
        self.windows = {}

        # Initialize auth window first
        self.init_auth_window()

        # Start with auth window
        self.show_window('AuthWindow')

    def init_auth_window(self):
        from presentation.windows.auth_window import AuthWindow
        auth_window = AuthWindow(self.container, self)
        self.windows['AuthWindow'] = auth_window
        auth_window.grid(row=0, column=0, sticky="nsew")

    def init_other_windows(self):
        """Initialize other windows after successful login"""
        from presentation.windows.dashboard import Dashboard
        from presentation.windows.booking_window import BookingWindow
        from presentation.windows.flight_window import FlightWindow
        from presentation.windows.crew_window import CrewWindow
        from presentation.windows.reports_window import ReportsWindow

        windows = {
            'Dashboard': Dashboard,
            'BookingWindow': BookingWindow,
            'FlightWindow': FlightWindow,
            'CrewWindow': CrewWindow,
            'ReportsWindow': ReportsWindow
        }

        for name, WindowClass in windows.items():
            if name not in self.windows:
                window = WindowClass(self.container, self)
                self.windows[name] = window
                window.grid(row=0, column=0, sticky="nsew")

    def show_window(self, window_name):
        """Show specified window with proper authentication checks"""
        # Always allow auth window
        if window_name == 'AuthWindow':
            if 'AuthWindow' not in self.windows:
                self.init_auth_window()
            self.windows['AuthWindow'].tkraise()
            return

        # For other windows, require authentication
        if not self.current_user:
            self.show_window('AuthWindow')
            return

        # Initialize other windows if not done yet
        if window_name not in self.windows:
            self.init_other_windows()

        # Show the requested window
        window = self.windows[window_name]
        window.tkraise()

        # Refresh window data if needed
        if hasattr(window, 'on_show'):
            window.on_show()

    def logout(self):
        """Proper logout handling"""
        # Clear current user
        self.current_user = None

        # Destroy all windows except AuthWindow
        for name, window in list(self.windows.items()):
            if name != 'AuthWindow':
                window.destroy()
                del self.windows[name]

        # Clear auth window fields
        if 'AuthWindow' in self.windows:
            auth_window = self.windows['AuthWindow']
            if hasattr(auth_window, 'login_username'):
                auth_window.login_username.delete(0, tk.END)
            if hasattr(auth_window, 'login_password'):
                auth_window.login_password.delete(0, tk.END)

        # Show auth window
        self.show_window('AuthWindow')