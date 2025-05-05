# presentation/main_gui.py
import tkinter as tk
from tkinter import ttk
from presentation.widgets import create_flight_tab, create_booking_tab, create_passenger_tab, create_crew_tab, \
    create_analytics_tab
from data_access.db_session import init_db


def launch_main_gui():
    init_db()
    root = tk.Tk()
    root.title("Airline Reservation System")
    root.geometry("1000x700")

    tab_control = ttk.Notebook(root)

    flight_tab = ttk.Frame(tab_control)
    booking_tab = ttk.Frame(tab_control)
    passenger_tab = ttk.Frame(tab_control)
    crew_tab = ttk.Frame(tab_control)
    analytics_tab = ttk.Frame(tab_control)

    tab_control.add(flight_tab, text='Flights')
    tab_control.add(booking_tab, text='Bookings')
    tab_control.add(passenger_tab, text='Passengers')
    tab_control.add(crew_tab, text='Crew')
    tab_control.add(analytics_tab, text='Analytics')

    tab_control.pack(expand=1, fill="both")

    create_flight_tab(flight_tab)
    create_booking_tab(booking_tab)
    create_passenger_tab(passenger_tab)
    create_crew_tab(crew_tab)
    create_analytics_tab(analytics_tab)

    root.mainloop()
