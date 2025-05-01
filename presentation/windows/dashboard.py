from tkinter import ttk


class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Center the content using an inner frame
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(expand=True)

        ttk.Label(center_frame, text="SkyLink Dashboard", font=('Arial', 16)).pack(pady=20)

        buttons = [
            ("Flight Management", self.open_flight_window),
            ("Booking Management", self.open_booking_window),
            ("Crew Management", self.open_crew_window),
            ("Reports", self.open_reports_window)
        ]

        for text, command in buttons:
            btn = ttk.Button(
                center_frame,
                text=text,
                command=command,
                width=25,
                style="Accent.TButton"
            )
            btn.pack(pady=10, ipady=5)

    def open_booking_window(self):
        self.controller.show_window('BookingWindow')

    def open_flight_window(self):
        self.controller.show_window('FlightWindow')

    def open_crew_window(self):
        from presentation.windows.crew_window import CrewWindow
        self.controller.show_window('CrewWindow')

    def open_reports_window(self):
        from presentation.windows.reports_window import ReportsWindow
        self.controller.show_window('ReportsWindow')