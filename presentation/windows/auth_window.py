import tkinter as tk
from tkinter import ttk


class AuthWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True)

        # Title
        ttk.Label(main_frame, text="SkyLink Airways", font=('Arial', 16, 'bold')).grid(row=0, column=0, pady=10)

        # Login frame
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding=10)
        login_frame.grid(row=1, column=0, padx=10, pady=10)

        # Username
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button
        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10, sticky=tk.E)

    def login(self):
        # TODO: Implement actual authentication
        from .dashboard import Dashboard
        dashboard = Dashboard(self.master, self.controller)
        dashboard.grid(row=0, column=0, sticky="nsew")
        dashboard.tkraise()