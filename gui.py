__author__ = "Mani"
import matplotlib

matplotlib.use("TkAgg")  # noqa: E402
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt

from tkinter import ttk
from datetime import date, timedelta
from logging import INFO as LOG_INFO
import os
import sys
import datetime

# https://pypi.org/project/tkcalendar/
# pip install tkcalendar
from tkcalendar import DateEntry

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

# Own modules imports

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402

sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402

from data_processor import DataProcessor
from color_logger import ColoredLogger
from plotter3 import Plotter3

MAIN_LOGGER = ColoredLogger(os.path.basename(__file__), LOG_INFO)


class TimePicker(ttk.Frame):
    def __init__(self, parent, default_hours, default_mins):
        super().__init__(parent)
        self.hourstr = tk.StringVar(self, str(default_hours))
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=2)
        self.minstr = tk.StringVar(self, str(default_mins))
        self.minstr.trace("w", self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstr, width=2)
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def trace_var(self, *args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get()) + 1 if self.hourstr.get() != "23" else 0)
        self.last_value = self.minstr.get()

    @staticmethod
    def show_error(title="Error", message="Error message"):
        messagebox.showerror(title, message)

    def get_time(self):
        if 23 < int(self.hourstr.get()) or int(self.hourstr.get()) < 0:
            self.show_error(
                title="Hour error",
                message="'{}' is not a valid hour.".format(int(self.hourstr.get())),
            )
        if 59 < int(self.minstr.get()) or int(self.minstr.get()) < 0:
            self.show_error(
                title="Hour error",
                message="'{}' is not a valid minute.".format(int(self.minstr.get())),
            )
        return "{:02d}:{:02d}".format(int(self.hourstr.get()), int(self.minstr.get()))


class MyDateEntry(DateEntry):
    def __init__(self, master=None, **kw):
        DateEntry.__init__(self, master=master, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg="black", bd=1)
        # add label displaying today's date below
        tk.Label(
            self._top_cal, bg="gray90", anchor="w", text="Today: %s" % date.today().strftime("%x")
        ).pack(fill="x")


class MainWindow(object):
    def __init__(self, main_window, c_logger=MAIN_LOGGER):

        self.c_logger = c_logger
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))
        self.main_window.title("Time report")
        self.c_logger.info("Set window title to 'Time report'")
        self.main_window.protocol("WM_DELETE_WINDOW", self.__disable_event)

        self.c_logger.info("Creating DataProcessor instance.")
        self.data_processor = DataProcessor(c_logger=MAIN_LOGGER)
        self.c_logger.info("DataProcessor instance successfully created.")

        self.__set_resizable()

        self.__create_new_record_gui_section()
        self.__create_visualisation_gui_section()

        self.__start_visualisation()

    def __disable_event(self):
        self.c_logger.warning("Showing error message box.")
        messagebox.showerror(
            title="Exit error", message="Please use the 'Exit' button instead of [X]!",
        )
        self.c_logger.info("Error message box has been closed.")

    def __set_resizable(self):
        self.c_logger.info("Starting to set the resizable rows and columns")
        for x in range(0, 11):
            self.c_logger.debug("Set the {}. row and column resizable.".format(x))
            self.main_window.grid_columnconfigure(x, weight=1)
            self.main_window.grid_rowconfigure(x, weight=1)
        self.c_logger.info("Successfully set the resizable rows and columns.")

    def __create_visualisation_gui_section(self):
        self.c_logger.info("Starting to create visualisation GUI section.")

        visualisation_label = ttk.Label(
            self.main_window, text="Visualisation", font=("Helvetica", 16)
        )
        visualisation_label.grid(row=5, column=0, columnspan=2)

        visualisation_from_date = ttk.Label(self.main_window, text="From")
        visualisation_from_date.grid(row=6, column=0)

        # Calculate the previous month to set the default 1 month visualisation.
        today = date.today()
        self.c_logger.info("Today: {}".format(today))
        previous_month = today - timedelta(days=30)
        self.c_logger.info("Previous 31 days: {}".format(previous_month))

        self.visualisation_from_calendar_instance = self.__set_calendar(set_date=previous_month)
        self.visualisation_from_calendar_instance.grid(row=6, column=1)

        visualisation_to_date = ttk.Label(self.main_window, text="To")
        visualisation_to_date.grid(row=7, column=0)

        self.visualisation_to_calendar_instance = self.__set_calendar()
        self.visualisation_to_calendar_instance.grid(row=7, column=1)

        set_button = ttk.Button(
            self.main_window,
            text="Start visualisation",
            command=lambda: self.__start_visualisation(),
        )
        set_button.grid(row=8, column=0, columnspan=2)

        set_button = ttk.Button(
            self.main_window, text="Exit", style="C.TButton", command=lambda: self.__quit(),
        )
        set_button.grid(row=9, column=0, columnspan=2)

        self.c_logger.info("Visualisation GUI section has been created successfully.")

    def __start_visualisation(self):

        self.c_logger.info("Starting visualisation.")

        from_date = self.__get_date_from_calendar(self.visualisation_from_calendar_instance)
        to_date = self.__get_date_from_calendar(self.visualisation_to_calendar_instance)
        date_range = self.data_processor.get_time_range(
            from_date.replace(" ", ""), to_date.replace(" ", "")
        )
        self.c_logger.info("Arriving date: {} , Leaving date: {}".format(from_date, to_date))
        self.c_logger.debug("Date range: {}".format(date_range))
        if len(date_range) > 31:
            self.c_logger.warning("Too many dates! Maximum days is 31!")
            messagebox.showerror(
                title="Too many dates",
                message="Maximum days is 31!\nPlease reduce your date range!",
            )
            self.c_logger.info("Error message box has been closed successfully.")
            return
        plotting_list = []
        self.c_logger.info("Starting to parse dates one by one.")
        for single_date in date_range:
            arriving, leaving = self.data_processor.get_arriving_leaving_times_based_on_date(
                single_date
            )
            if not arriving or not leaving:
                self.c_logger.warning(
                    "There is no arriving of leaving time for '()' date.".format(single_date)
                )
                arriving = "00:00"
                leaving = "00:00"
            self.c_logger.info(
                "Date: {} ; Arriving: {} ; Leaving: {}".format(single_date, arriving, leaving)
            )

            plotting_list.append({"date": single_date, "from": arriving, "to": leaving})
        self.c_logger.debug("Created plotting list: {}".format(plotting_list))
        self.c_logger.info("Starting to create 'Plotter3' instance.")
        self.plotter3 = Plotter3(plotting_list, c_logger=self.c_logger)
        self.c_logger.info("'Plotter3' instance has been created successfully.")
        self.c_logger.info("Starting to get the figure object.")
        self.plotterobj = self.plotter3.plotting()
        self.c_logger.info("Geting figure: {}".format(self.plotterobj))
        self.c_logger.info("Starting to plot the figure to TK canvas.")
        self.plot()
        self.c_logger.info("The figure has been successfully plotted to TK canvas.")

    def __quit(self):
        self.c_logger.info("Quit from application.")
        self.main_window.quit()

    def __create_new_record_gui_section(self):
        self.c_logger.info("Starting to create the new record setting GUI section.")
        create_label = ttk.Label(
            self.main_window, text="Create/Update data", font=("Helvetica", 16)
        )
        create_label.grid(row=0, column=0, columnspan=2)

        new_data_date_label = ttk.Label(self.main_window, text="Date")
        new_data_date_label.grid(row=1, column=0)

        self.new_data_calendar_instance = self.__set_calendar()
        self.new_data_calendar_instance.grid(row=1, column=1)

        arrive_time_label = ttk.Label(self.main_window, text="Arriving")
        arrive_time_label.grid(row=2, column=0)

        self.arrive_time_picker_instance = self.__set_time_picker("9", "0")
        self.arrive_time_picker_instance.grid(row=2, column=1)

        leaving_time_label = ttk.Label(self.main_window, text="Leaving")
        leaving_time_label.grid(row=3, column=0)

        self.leaving_time_picker_instance = self.__set_time_picker("17", "20")
        self.leaving_time_picker_instance.grid(row=3, column=1)

        set_button = ttk.Button(
            self.main_window,
            text="Set new record",
            command=lambda: self.__set_time_into_config_json(),
        )
        set_button.grid(row=4, column=0, columnspan=2)

        self.c_logger.info("New record setting GUI section has been successfully created.")

    def __set_time_into_config_json(self):
        self.c_logger.info("Starting to set the times into Json file.")
        current_selected_date = self.__get_date_from_calendar(self.new_data_calendar_instance)
        arriving_time = self.__get_time_from_time_picker(self.arrive_time_picker_instance)
        leaving_time = self.__get_time_from_time_picker(self.leaving_time_picker_instance)
        self.c_logger.info(
            "Current selected date: {} , Arriving: {} , Leaving: {}".format(
                current_selected_date, arriving_time, leaving_time
            )
        )
        self.c_logger.info("Starting to set the new record into Json file.")
        self.data_processor.set_time(
            current_selected_date.replace(" ", ""), arriving_time, leaving_time
        )

        self.c_logger.info("Successfully set the times into Json file.")

    def __set_time_picker(self, default_hours, default_mins):
        self.c_logger.info("Setting the time picker.")
        self.c_logger.info(
            "Default hours: {} , Default minutes: {}".format(default_hours, default_mins)
        )
        self.c_logger.info("Starting to create 'TimePicker' instance.")
        return_instance = TimePicker(self.main_window, str(default_hours), str(default_mins))
        self.c_logger.info("'TimePicker' instance has been created successfully.")
        return return_instance

    def __set_calendar(self, set_date=None):
        self.c_logger.info("Starting to set the calendar.")
        if not set_date:
            set_date = datetime.datetime.now()
        self.c_logger.info("Getting set date: {}".format(set_date))
        self.c_logger.info("Starting to create 'MyDateEntry' instance.")
        return_instance = MyDateEntry(
            master=self.main_window,
            year=set_date.year,
            month=set_date.month,
            day=set_date.day,
            selectbackground="gray80",
            selectforeground="black",
            normalbackground="white",
            normalforeground="black",
            background="gray90",
            foreground="black",
            bordercolor="gray90",
            othermonthforeground="gray50",
            othermonthbackground="white",
            othermonthweforeground="gray50",
            othermonthwebackground="white",
            weekendbackground="white",
            weekendforeground="black",
            headersbackground="white",
            headersforeground="gray70",
        )

        self.c_logger.info("'MyDateEntry' instance has been created successfully.")

        return return_instance

    def __get_date_from_calendar(self, calendar_instance):
        self.c_logger.info("Staring to get date from calendar.")
        self.c_logger.debug("The getting calendar instance: {}".format(calendar_instance))
        date_from_calendar = calendar_instance.get()
        self.c_logger.info("Successfully get the date from calendar.")
        self.c_logger.debug("The getting date from calendar: {}".format(date_from_calendar))
        return date_from_calendar

    def __get_time_from_time_picker(self, time_picker_instance):
        self.c_logger.info("Staring to get time from time picker.")
        self.c_logger.debug("The getting time picker instance: {}".format(time_picker_instance))
        time_from_time_picker = time_picker_instance.get_time()
        self.c_logger.info("Successfully get the time from time picker.")
        self.c_logger.debug("The getting time from time picker: {}".format(time_from_time_picker))
        return time_from_time_picker

    def plot(self):
        self.c_logger.info("Starting to plot the figure onto TK canvas.")
        canvas = FigureCanvasTkAgg(self.plotterobj, master=self.main_window)
        self.c_logger.info("The figure has been plotted onto TK canvas successfully.")
        self.c_logger.debug("The 'FigureCanvasTkAgg' object: {}".format(canvas))
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, sticky="nsew")
        canvas.draw()
        self.c_logger.info("The complete figure has been integrated into GUI successfully.")


window = tk.Tk()
# change ttk theme to 'clam' to fix issue with downarrow button
style = ttk.Style(window)
style.theme_use("alt")
style.configure("BW.TLabel", foreground="black", background="white")
style.configure(
    "C.TButton", font=("calibri", 12, "bold"), background="red",
)

start = MainWindow(window)
window.mainloop()
