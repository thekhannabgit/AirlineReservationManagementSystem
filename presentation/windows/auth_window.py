import tkinter as tk
from tkinter import ttk, messagebox

from sqlalchemy.exc import NoResultFound

from database.models import UserRole
from business_logic.auth_services import AuthService

class AuthWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="SkyLink Airways",
                  style="Title.TLabel").grid(row=0, column=0, pady=20, columnspan=2)

        # Notebook for login/register tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, pady=10)

        # Login tab
        login_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(login_frame, text="Login")

        # Register tab
        register_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(register_frame, text="Register")

        # Login form
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_username = ttk.Entry(login_frame)
        self.login_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.login_password = ttk.Entry(login_frame, show="*")
        self.login_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            login_frame,
            text="Login",
            command=self.login,
            style="Accent.TButton"
        ).grid(row=2, column=1, pady=10, sticky=tk.E)

        # Register form
        ttk.Label(register_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.register_username = ttk.Entry(register_frame)
        self.register_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.register_password = ttk.Entry(register_frame, show="*")
        self.register_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.register_confirm = ttk.Entry(register_frame, show="*")
        self.register_confirm.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.register_email = ttk.Entry(register_frame)
        self.register_email.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(
            register_frame,
            text="Register",
            command=self.register,
            style="Accent.TButton"
        ).grid(row=4, column=1, pady=10, sticky=tk.E)

        # Configure grid weights
        for frame in [login_frame, register_frame]:
            frame.columnconfigure(1, weight=1)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning("Validation", "Username and password are required")
            return

        try:
            auth_service = AuthService(self.controller.session)
            user, message = auth_service.authenticate_user(username, password)

            if user:
                self.controller.current_user = user
                self.controller.init_other_windows()
                self.controller.show_window('Dashboard')
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def register(self):
        username = self.register_username.get()
        password = self.register_password.get()
        confirm = self.register_confirm.get()
        email = self.register_email.get()

        if not username or not password or not confirm or not email:
            messagebox.showwarning("Validation", "All fields are required")
            return

        if password != confirm:
            messagebox.showwarning("Validation", "Passwords do not match")
            return

        try:
            auth_service = AuthService(self.controller.session)
            success, message = auth_service.register_user(
                username=username,
                password=password,
                email=email,
                role=UserRole.USER  # Explicitly set to regular user
            )

            if success:
                messagebox.showinfo("Success", message)
                self.notebook.select(0)  # Switch to login tab
                self.login_username.delete(0, tk.END)
                self.login_username.insert(0, username)
                self.login_password.focus()
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")