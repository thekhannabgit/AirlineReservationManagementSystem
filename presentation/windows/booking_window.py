import tkinter as tk
from tkinter import ttk, messagebox
from presentation.dialogs.booking_dialog import BookingDialog
from database.models import Flight, Airport, FlightStatus


class BookingWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()
        self.load_flights()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Available Flights", font=('Arial', 14)).pack(pady=10)

        # Treeview with scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("flight", "departure", "arrival", "time", "status"),
            show="headings",
            height=10
        )

        # Configure columns
        self.tree.heading("flight", text="Flight #")
        self.tree.heading("departure", text="From")
        self.tree.heading("arrival", text="To")
        self.tree.heading("time", text="Departure Time")
        self.tree.heading("status", text="Status")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("flight", width=100, anchor=tk.CENTER)
        self.tree.column("departure", width=150, anchor=tk.W)
        self.tree.column("arrival", width=150, anchor=tk.W)
        self.tree.column("time", width=150, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Book button
        ttk.Button(
            main_frame,
            text="Book Selected Flight",
            command=self.book_flight,
            style="Accent.TButton"
        ).pack(pady=10)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack()

    def load_flights(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Load flights with airport information
            flights = self.session.query(Flight) \
                .join(Airport, Flight.departure_airport_code == Airport.code) \
                .filter(Flight.status == FlightStatus.SCHEDULED) \
                .all()

            if not flights:
                print("DEBUG: No scheduled flights found")
                return

            print(f"DEBUG: Found {len(flights)} flights to display")

            for flight in flights:
                self.tree.insert("", "end", values=(
                    flight.flight_number,
                    f"{flight.departure_airport.code} ({flight.departure_airport.city})",
                    f"{flight.arrival_airport.code} ({flight.arrival_airport.city})",
                    flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                    flight.status.value
                ))

        except Exception as e:
            print(f"Error loading flights: {e}")
            messagebox.showerror("Error", "Failed to load flights")

    def book_flight(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Please select a flight first")
            return

        flight_data = self.tree.item(selected)['values']
        BookingDialog(self, self.session, flight_data[0], self.load_flights)