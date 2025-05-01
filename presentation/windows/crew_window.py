from tkinter import ttk
from database.models import Crew


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

        ttk.Label(main_frame, text="Crew Management", font=('Arial', 14)).pack(pady=10)

        # Crew Treeview
        self.tree = ttk.Treeview(main_frame, columns=("name", "role", "email"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("email", text="Email")
        self.tree.pack(fill="both", expand=True, pady=10)

        # Back button
        ttk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: self.controller.show_window('Dashboard')
        ).pack()

    def load_crew(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        crew_members = self.session.query(Crew).all()
        for crew in crew_members:
            self.tree.insert("", "end", values=(
                f"{crew.first_name} {crew.last_name}",
                crew.role.value,
                crew.email
            ))