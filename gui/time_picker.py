"""
This module contains the all Time picker related attributes.
"""

from tkinter import ttk
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox


class TimePicker(ttk.Frame):
    """
    Time picker Class.
    It is inherited from ttk.Frame class.
    It contains all Time picker related attributes.
    https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Frame.html
    Examples:
        https://www.programcreek.com/python/example/82813/ttk.Frame
    """

    def __init__(self, parent, default_hours, default_mins):
        """
        Init method of the 'TimePicker' class.
        :param parent: Instance of the parent TK.
        :param default_hours: Default hours to time picker object.
        :param default_mins: Default minutes to time picker object.
        """

        super().__init__(parent)
        self.hourstr = tk.StringVar(self, str(default_hours))
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=2)
        self.minstr = tk.StringVar(self, str(default_mins))
        self.minstr.trace("w", self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstr, width=2)
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def trace_var(self):
        """
        Count the hours in case of 59 minutes.
        :return: None
        """

        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get()) + 1 if self.hourstr.get() != "23" else 0)
        self.last_value = self.minstr.get()

    @staticmethod
    def show_error(title="Error", message="Error message"):
        """
        Show an error message box.
        :param title: Title of the error message box.
        :param message: Message (content) of the error message box.
        :return: None
        """

        messagebox.showerror(title, message)

    def get_time(self):
        """
        This method provides the current time (Value of Time picker).
        :return: The current time as a string. Time Format: {:02d}:{:02d}
        """

        # If the hour counter is greater than 23 or it is less than 0.
        if 23 < int(self.hourstr.get()) or int(self.hourstr.get()) < 0:
            # Show an error message box and return nothing.
            self.show_error(
                title="Hour error",
                message="'{}' is not a valid hour.".format(int(self.hourstr.get())),
            )
            return None
        # If the minute counter is greater than 59 or it is less than 0.
        if 59 < int(self.minstr.get()) or int(self.minstr.get()) < 0:
            # Show an error message box and return nothing.
            self.show_error(
                title="Hour error",
                message="'{}' is not a valid minute.".format(int(self.minstr.get())),
            )
            return None
        # The ranges of hour and minute counters are valid so return the values.
        return "{:02d}:{:02d}".format(int(self.hourstr.get()), int(self.minstr.get()))
