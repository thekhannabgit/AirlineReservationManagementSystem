import tkinter as tk
from tkinter import ttk
from database.models import Booking


class BookingWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Main notebook
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create booking tab
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="New Booking")

        # View bookings tab
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="My Bookings")

        # Back button
        ttk.Button(self, text="Back", command=self.go_back).pack(side=tk.BOTTOM, pady=5)

    def go_back(self):
        from .dashboard import Dashboard
        dashboard = Dashboard(self.master, self.controller)
        dashboard.grid(row=0, column=0, sticky="nsew")
        dashboard.tkraise()