from tkinter import ttk
import tkinter as tk


def configure_styles():
    style = ttk.Style()

    # Configure the theme
    style.theme_create("skylink", parent="alt", settings={
        "TFrame": {
            "configure": {
                "background": "#f0f8ff",  # Alice blue
                "borderwidth": 0
            }
        },
        "TLabel": {
            "configure": {
                "background": "#f0f8ff",
                "foreground": "#003366",  # Dark blue
                "font": ('Arial', 10)
            }
        },
        "TButton": {
            "configure": {
                "background": "#4682b4",  # Steel blue
                "foreground": "white",
                "font": ('Arial', 10),
                "padding": 8,
                "borderwidth": 1,
                "relief": "raised"
            },
            "map": {
                "background": [("active", "#5f9ea0"), ("disabled", "#d3d3d3")],
                "foreground": [("disabled", "#a9a9a9")]
            }
        },
        "Treeview": {
            "configure": {
                "background": "white",
                "fieldbackground": "white",
                "font": ('Arial', 9),
                "rowheight": 25
            }
        },
        "Treeview.Heading": {
            "configure": {
                "background": "#4682b4",
                "foreground": "white",
                "font": ('Arial', 10, 'bold'),
                "padding": 5
            }
        },
        "TCombobox": {
            "configure": {
                "selectbackground": "white",
                "selectforeground": "black",
                "fieldbackground": "white",
                "background": "white",
                "foreground": "black"
            }
        },
        "TEntry": {
            "configure": {
                "fieldbackground": "white",
                "foreground": "black",
                "insertcolor": "black"
            }
        }
    })

    style.theme_use("skylink")

    # Custom styles
    style.configure("Accent.TButton",
                    background="#5f9ea0",  # Cadet blue
                    foreground="white",
                    font=('Arial', 10, 'bold'),
                    padding=10)

    style.configure("Title.TLabel",
                    font=('Arial', 16, 'bold'),
                    foreground="#003366")

    style.configure("Subtitle.TLabel",
                    font=('Arial', 12, 'bold'),
                    foreground="#4682b4")

    style.map("Accent.TButton",
              background=[("active", "#5f9ea0"), ("pressed", "#2f4f4f")])

    # Configure ttk widgets to use our theme
    style.configure("TNotebook", background="#f0f8ff")
    style.configure("TNotebook.Tab",
                    background="#4682b4",
                    foreground="white",
                    padding=[10, 5])
    style.map("TNotebook.Tab",
              background=[("selected", "#5f9ea0")],
              foreground=[("selected", "white")])