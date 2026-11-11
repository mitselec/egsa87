"""Simple Tkinter GUI for the egsa87 package.

Run with:

    egsa87-gui

or:

    python -m egsa87.gui

On Linux the tkinter module requires the python3-tk package
(e.g. ``sudo apt install python3-tk``); on Windows and macOS it ships
with the standard Python installation.
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk

from .egsa87wgs84 import egsa87wgs84
from .wgs84egsa87 import wgs84egsa87

# Supported conversion directions, in display order.
MODES = ("WGS84 → EGSA87", "EGSA87 → WGS84")

_FORWARD_LABELS = ("Latitude (°)", "Longitude (°)")
_INVERSE_LABELS = ("X (m)", "Y (m)")


def wgs84_to_egsa87_degrees(lat, lon):
    """Convert WGS84 latitude/longitude in degrees to EGSA87 x/y in meters."""
    return wgs84egsa87(math.radians(lat), math.radians(lon))


def egsa87_to_wgs84_degrees(x, y):
    """Convert EGSA87 x/y in meters to WGS84 latitude/longitude in degrees."""
    phi, lambd = egsa87wgs84(x, y)
    return math.degrees(phi), math.degrees(lambd)


def convert(mode, first, second):
    """Run the conversion for the selected mode.

    ``first``/``second`` are the two raw user inputs (strings or numbers).
    Returns a (value1, value2) tuple: EGSA87 (x, y) in meters for the forward
    mode, WGS84 (latitude, longitude) in degrees for the inverse mode.

    Raises ValueError on non-numeric input. A decimal comma is accepted as
    a thousands-agnostic decimal separator, since it is customary in Greece.
    """
    try:
        a = float(str(first).strip().replace(",", "."))
        b = float(str(second).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Please enter valid numbers.") from None

    if mode == MODES[0]:
        return wgs84_to_egsa87_degrees(a, b)
    return egsa87_to_wgs84_degrees(a, b)


class ConverterApp:
    def __init__(self, root):
        self.root = root
        root.title("egsa87 converter")
        root.resizable(False, False)

        self.mode = tk.StringVar(value=MODES[0])
        self.first_var = tk.StringVar()
        self.second_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self._last_result = None

        main = ttk.Frame(root, padding=12)
        main.grid(row=0, column=0)

        for row, text in enumerate(MODES):
            ttk.Radiobutton(
                main, text=text, value=text, variable=self.mode,
                command=self._on_mode_change,
            ).grid(row=row, column=0, columnspan=3, sticky="w")

        self._input_frame = ttk.Frame(main, padding=(0, 8))
        self._input_frame.grid(row=2, column=0, columnspan=3)

        self._first_label = ttk.Label(self._input_frame)
        self._first_label.grid(row=0, column=0, sticky="w", padx=(0, 6))
        ttk.Entry(self._input_frame, width=16, textvariable=self.first_var).grid(
            row=0, column=1, padx=(0, 12)
        )
        self._second_label = ttk.Label(self._input_frame)
        self._second_label.grid(row=0, column=2, sticky="w", padx=(0, 6))
        ttk.Entry(self._input_frame, width=16, textvariable=self.second_var).grid(
            row=0, column=3
        )

        ttk.Button(main, text="Convert", command=self._on_convert).grid(
            row=3, column=0, columnspan=2, sticky="w"
        )
        ttk.Button(main, text="Copy result", command=self._on_copy).grid(
            row=3, column=2, sticky="e"
        )

        ttk.Label(main, textvariable=self.result_var, padding=(0, 10)).grid(
            row=4, column=0, columnspan=3, sticky="w"
        )

        root.bind("<Return>", self._on_convert)
        self._on_mode_change()

    def _on_mode_change(self):
        labels = _FORWARD_LABELS if self.mode.get() == MODES[0] else _INVERSE_LABELS
        self._first_label.config(text=labels[0])
        self._second_label.config(text=labels[1])
        self.result_var.set("")
        self._last_result = None

    def _on_convert(self, event=None):
        try:
            value1, value2 = convert(
                self.mode.get(), self.first_var.get(), self.second_var.get()
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        if self.mode.get() == MODES[0]:
            self.result_var.set(f"X = {value1:.3f} m    Y = {value2:.3f} m")
        else:
            self.result_var.set(f"lat = {value1:.7f}°    lon = {value2:.7f}°")
        self._last_result = (value1, value2)

    def _on_copy(self):
        if self._last_result is None:
            return
        text = "{:.6f} {:.6f}".format(*self._last_result)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)


def build_app(root=None):
    """Create the application window. Returns the (root, app) pair."""
    if root is None:
        root = tk.Tk()
    app = ConverterApp(root)
    return root, app


def main():
    root, _app = build_app()
    root.mainloop()


if __name__ == "__main__":
    main()
