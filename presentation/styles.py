from tkinter import ttk


def configure_styles():
    style = ttk.Style()

    # Main styles
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)

    # Accent button
    style.configure('Accent.TButton',
                    foreground='white',
                    background='#0078d7',
                    font=('Arial', 10, 'bold'))

    # Treeview styles
    style.configure('Treeview', font=('Arial', 9), rowheight=25)
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))