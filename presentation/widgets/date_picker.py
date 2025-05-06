import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class DatePicker(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.date_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.entry = ttk.Entry(self, textvariable=self.date_var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            self,
            text="📅",
            command=self.show_calendar,
            width=3
        ).pack(side=tk.LEFT)

    def show_calendar(self):
        top = tk.Toplevel(self)
        top.title("Select Date")

        cal = Calendar(
            top,
            selectmode='day',
            date_pattern='yyyy-mm-dd'
        )
        cal.pack(pady=10)

        if self.date_var.get():
            try:
                cal.selection_set(datetime.strptime(self.date_var.get(), "%Y-%m-%d"))
            except:
                pass

        def set_date():
            self.date_var.set(cal.get_date())
            top.destroy()

        ttk.Button(
            top,
            text="OK",
            command=set_date
        ).pack(pady=5)

    def get_date(self):
        return self.date_var.get()

    def set_date(self, date_str):
        self.date_var.set(date_str)