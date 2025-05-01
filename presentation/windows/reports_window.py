from tkinter import ttk
from tkinter import messagebox


class ReportsWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Analytics Reports", font=('Arial', 14)).pack(pady=10)

        # Report buttons
        ttk.Button(
            main_frame,
            text="Flight Occupancy Report",
            command=self.show_occupancy_report
        ).pack(pady=10)

        ttk.Button(
            main_frame,
            text="Revenue Report",
            command=self.show_revenue_report
        ).pack(pady=10)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack()

    def show_occupancy_report(self):
        messagebox.showinfo("Info", "Flight occupancy report will be shown here")

    def show_revenue_report(self):
        messagebox.showinfo("Info", "Revenue report will be shown here")