import tkinter as tk
from tkinter import ttk


class CrewWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Crew management UI
        label = ttk.Label(self, text="Crew Management", font=('Arial', 14))
        label.pack(pady=10)

        # Back button
        ttk.Button(self, text="Back", command=self.go_back).pack(side=tk.BOTTOM, pady=5)

    def go_back(self):
        from .dashboard import Dashboard
        dashboard = Dashboard(self.master, self.controller)
        dashboard.grid(row=0, column=0, sticky="nsew")
        dashboard.tkraise()