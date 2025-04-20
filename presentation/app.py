import tkinter as tk
from tkinter import ttk
from .styles import configure_styles
from .windows.auth_window import AuthWindow


class AirlineApp(tk.Tk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.title("SkyLink Airways")
        self.geometry("1200x800")
        configure_styles()

        # Main container
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize auth window
        self.auth_window = AuthWindow(container, self)
        self.auth_window.grid(row=0, column=0, sticky="nsew")

        # Show auth window initially
        self.auth_window.tkraise()


if __name__ == "__main__":
    from database.initialization import initialize_database
    from sqlalchemy.orm import sessionmaker

    engine = initialize_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    app = AirlineApp(session)
    app.mainloop()
    session.close()