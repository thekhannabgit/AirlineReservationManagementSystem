import tkinter as tk
from tkinter import ttk, messagebox


class PassengerDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Passenger Details")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Form fields
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Passport Number", "passport_number")
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label + ":").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(main_frame)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=2)
            self.entries[field] = entry

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Submit", command=self.submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        if all(data.values()):  # Simple validation
            self.callback(data)
            self.destroy()
        else:
            messagebox.showwarning("Validation", "All fields are required!")