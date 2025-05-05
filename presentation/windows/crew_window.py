# presentation/windows/crew_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Crew, CrewRole
from presentation.dialogs.crew_dialog import CrewDialog

class CrewWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.session = controller.session
        self.create_widgets()
        self.load_crew()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Crew Management", style="Title.TLabel").pack(pady=10)

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)

        ttk.Button(
            btn_frame,
            text="Add Crew Member",
            command=self.add_crew,
            style="Accent.TButton"
        ).pack(side="left")

        ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_crew
        ).pack(side="left", padx=5)

        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "role", "email"),
            show="headings",
            height=10
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("email", text="Email")

        self.tree.column("name", width=200)
        self.tree.column("role", width=150)
        self.tree.column("email", width=250)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack(pady=10)

    def load_crew(self):
        self.tree.delete(*self.tree.get_children())
        try:
            crew_members = self.session.query(Crew).order_by(Crew.last_name, Crew.first_name).all()
            for crew in crew_members:
                self.tree.insert("", "end", values=(
                    f"{crew.first_name} {crew.last_name}",
                    crew.role.value,
                    crew.email
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load crew: {str(e)}")

    def add_crew(self):
        CrewDialog(self, self.session, callback=self.load_crew)