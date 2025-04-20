from tkinter import ttk


def configure_styles():
    style = ttk.Style()

    # Main styles
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)

    # Treeview styles
    style.configure('Treeview', font=('Arial', 9), rowheight=25)
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    style.map('Treeview', background=[('selected', '#0078d7')])

    # Entry styles
    style.configure('TEntry', padding=5)

    # Notebook styles
    style.configure('TNotebook', background='#f5f5f5')
    style.configure('TNotebook.Tab', padding=(10, 5))