# presentation/dialogs/crew_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Crew, CrewRole


class CrewDialog(tk.Toplevel):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback

        self.title("Add Crew Member")
        self.geometry("400x300")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Role:", "role")
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)

            if field == "role":
                self.role_var = tk.StringVar()
                role_dropdown = ttk.Combobox(
                    main_frame,
                    textvariable=self.role_var,
                    values=[role.value for role in CrewRole],
                    state="readonly"
                )
                role_dropdown.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                role_dropdown.current(0)
                self.entries[field] = self.role_var
            else:
                entry = ttk.Entry(main_frame)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                self.entries[field] = entry

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        ttk.Button(
            btn_frame,
            text="Save",
            command=self.save_crew,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", padx=5)

        main_frame.columnconfigure(1, weight=1)

    def save_crew(self):
        try:
            crew = Crew(
                first_name=self.entries["first_name"].get(),
                last_name=self.entries["last_name"].get(),
                email=self.entries["email"].get(),
                role=CrewRole(self.entries["role"].get())
            )

            self.session.add(crew)
            self.session.commit()

            messagebox.showinfo("Success", "Crew member added successfully")
            self.callback()
            self.destroy()

        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Failed to save crew member: {str(e)}")