"""
This module contains the all Date entry related attributes.
"""

# Documentation: https://pypi.org/project/tkcalendar/
# Install it: pip install tkcalendar
from tkcalendar import DateEntry
from datetime import date

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class MyDateEntry(DateEntry):
    """
    Date Entry class.
    This class contains all Date Entry related attributes.
    It is inherited from 'DateEntry' class (Comes from 'tkcalendar' module).
    # Documentation: https://pypi.org/project/tkcalendar/
    # Install it: pip install tkcalendar
    """

    def __init__(self, master=None, **kw):
        """
        Init method of the 'MyDateEntry' class.
        :param master: Instance of the main Tk window.
        :param kw: Pass all key-word arguments.
        """

        DateEntry.__init__(self, master=master, **kw)
        # Add black border around drop-down calendar
        self._top_cal.configure(bg="black", bd=1)
        # Add label displaying today's date below
        tk.Label(
            self._top_cal, bg="gray90", anchor="w", text="Today: %s" % date.today().strftime("%x")
        ).pack(fill="x")
