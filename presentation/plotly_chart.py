# presentation/plotly_chart.py
import tkinter as tk
from tkinter import ttk
import plotly.graph_objects as go
from plotly.offline import plot
import tempfile
import os
import webbrowser
from threading import Thread


class PlotlyChart(ttk.Frame):
    def __init__(self, parent, figure, **kwargs):
        super().__init__(parent, **kwargs)
        self.figure = figure
        self.create_widgets()

    def create_widgets(self):
        # Create HTML file with the plot
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        plot(self.figure, filename=self.temp_file.name, auto_open=False)

        # Create web view
        self.webview = tk.Frame(self)
        self.webview.pack(fill="both", expand=True)

        # Open in browser button
        ttk.Button(
            self,
            text="Open in Browser",
            command=self.open_in_browser,
            style="Accent.TButton"
        ).pack(pady=5)

    def open_in_browser(self):
        def _open():
            webbrowser.open(f"file://{os.path.abspath(self.temp_file.name)}")

        Thread(target=_open).start()

    def __del__(self):
        if hasattr(self, 'temp_file'):
            try:
                self.temp_file.close()
                os.unlink(self.temp_file.name)
            except:
                pass