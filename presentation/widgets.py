# presentation/widgets.py
import tkinter as tk
from tkinter import ttk, messagebox
from business_logic import flight_manager, booking_manager, passenger_manager, crew_manager
from presentation.charts import show_analytics_chart

def create_flight_tab(tab):
    fields = ['Flight No', 'Source', 'Destination', 'Departure Time (YYYY-MM-DD HH:MM)', 'Capacity']
    entries = {}

    for i, label in enumerate(fields):
        ttk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entries[label] = ttk.Entry(tab, width=40)
        entries[label].grid(row=i, column=1, padx=10, pady=5)

    def add_flight():
        try:
            flight_manager.add_flight(
                entries['Flight No'].get(),
                entries['Source'].get(),
                entries['Destination'].get(),
                entries['Departure Time (YYYY-MM-DD HH:MM)'].get(),
                int(entries['Capacity'].get())
            )
            messagebox.showinfo("Success", "Flight added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(tab, text="Add Flight", command=add_flight).grid(row=len(fields), column=1, pady=10)

def create_booking_tab(tab):
    labels = ['Booking Ref', 'Flight No', 'Passenger Name', 'Email', 'Phone']
    entries = {}

    for i, label in enumerate(labels):
        ttk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entries[label] = ttk.Entry(tab, width=40)
        entries[label].grid(row=i, column=1, padx=10, pady=5)

    def book_flight():
        try:
            booking_manager.book_flight(
                entries['Booking Ref'].get(),
                entries['Flight No'].get(),
                entries['Passenger Name'].get(),
                entries['Email'].get(),
                entries['Phone'].get()
            )
            messagebox.showinfo("Success", "Booking successful!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(tab, text="Book Flight", command=book_flight).grid(row=len(labels), column=1, pady=10)

def create_passenger_tab(tab):
    tree = ttk.Treeview(tab, columns=("ID", "Name", "Email", "Phone"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_passengers():
        for row in tree.get_children():
            tree.delete(row)
        for p in passenger_manager.get_all_passengers():
            tree.insert("", "end", values=(p.id, p.name, p.email, p.phone))

    ttk.Button(tab, text="Load Passengers", command=refresh_passengers).pack(pady=5)

def create_crew_tab(tab):
    fields = ['Name', 'Role', 'Flight No']
    entries = {}

    for i, label in enumerate(fields):
        ttk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entries[label] = ttk.Entry(tab, width=40)
        entries[label].grid(row=i, column=1, padx=10, pady=5)

    def add_crew():
        try:
            crew_manager.add_crew(
                entries['Name'].get(),
                entries['Role'].get(),
                entries['Flight No'].get()
            )
            messagebox.showinfo("Success", "Crew member added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(tab, text="Add Crew", command=add_crew).grid(row=len(fields), column=1, pady=10)

def create_analytics_tab(tab):
    ttk.Button(tab, text="Show Analytics Charts", command=show_analytics_chart).pack(pady=20)
