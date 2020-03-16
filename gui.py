"""
This is the main script and it contains the all main window attributes.
Python3.6.x > Python version is required.
"""

__author__ = "milanbalazs"
import matplotlib
import os
import sys
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from datetime import date, timedelta


# Documentation: https://pypi.org/project/tkcalendar/
# Install it: pip install tkcalendar
from tkcalendar import DateEntry

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402
# Append the current directory to PATH
sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402

# Own modules imports
from data_processor import DataProcessor
from color_logger import ColoredLogger
from plotter3 import Plotter3

# Set-up the main logger instance.
PATH_OF_LOG_FILE = os.path.join(PATH_OF_FILE_DIR, "logs", "main_log.log")
MAIN_LOGGER = ColoredLogger(os.path.basename(__file__), log_file_path=PATH_OF_LOG_FILE)

# Set path of the window icon
PATH_OF_WINDOW_ICON = os.path.join(PATH_OF_FILE_DIR, "imgs", "window_icon.png")
matplotlib.use("TkAgg")

# Set test data set
TEST_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "conf", "time_data_test.json")


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


class MainWindow(object):
    """
    This class contains the all Main Window related attributes.
    """

    def __init__(self, main_window, c_logger=MAIN_LOGGER):
        """
        Init method of the 'MainWindow' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        """

        self.c_logger = c_logger
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))

        self.c_logger.info("Creating DataProcessor instance.")
        if test_run:
            self.data_processor = DataProcessor(c_logger=MAIN_LOGGER, config=TEST_CONFIG_FILE)
        else:
            self.data_processor = DataProcessor(c_logger=MAIN_LOGGER)
        self.c_logger.info("DataProcessor instance successfully created.")

        self.__set_resizable()

        self.__create_new_record_gui_section()
        self.__create_visualisation_gui_section()

        self.__start_visualisation()

    def __set_resizable(self):
        """
        The the rows and columns to be configurable (resizable).
        10 rows and 10 columns are set to resizable.
        :return: None
        """

        self.c_logger.info("Starting to set the resizable rows and columns")
        for x in range(0, 11):
            self.c_logger.debug("Set the {}. row and column resizable.".format(x))
            self.main_window.grid_columnconfigure(x, weight=1)
            self.main_window.grid_rowconfigure(x, weight=1)
        self.c_logger.info("Successfully set the resizable rows and columns.")

    def __create_visualisation_gui_section(self):
        """
        Create the visualisation related GUI section and render it to the main window.
        :return: None
        """

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
            self.main_window, text="Exit", style="C.TButton", command=lambda: self.quit_from_app(),
        )
        set_button.grid(row=9, column=0, columnspan=2)

        self.c_logger.info("Visualisation GUI section has been created successfully.")

    def __start_visualisation(self):
        """
        Get all needed data for visualisation and plot it.
        The plotted Matplotlib figure is integrated into the Main Window.
        :return: None
        """

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

    def quit_from_app(self):
        """
        Quit from application.
        :return: None
        """

        self.c_logger.info("Quit from application.")
        self.main_window.quit()

    def __create_new_record_gui_section(self):
        """
        Create the visualisation related GUI section and render it to the main window.
        :return: None
        """

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
        """
        This method is a callback of the button which triggers to set a new time record.
        The new time record is save to the config file (Json).
        :return: None
        """

        self.c_logger.info("Starting to set the times into Json file.")
        current_selected_date = self.__get_date_from_calendar(self.new_data_calendar_instance)
        arriving_time = self.__get_time_from_time_picker(self.arrive_time_picker_instance)
        leaving_time = self.__get_time_from_time_picker(self.leaving_time_picker_instance)
        self.c_logger.info(
            "Current selected date: {} , Arriving: {} , Leaving: {}".format(
                current_selected_date, arriving_time, leaving_time
            )
        )
        if not arriving_time or not leaving_time:
            self.c_logger.error(
                "The set arriving/leaving time was not valid. "
                "The record won't be set to data-set."
            )
            return
        if not self.data_processor.validate_time_range(arriving_time, leaving_time):
            error_msg = (
                "The getting time range is not correct. "
                "The arriving time is earlier than leaving."
            )
            self.c_logger.error(error_msg)
            messagebox.showerror("Wring time range", error_msg)
            return
        self.c_logger.info("Starting to set the new record into Json file.")
        self.data_processor.set_time(
            current_selected_date.replace(" ", ""), arriving_time, leaving_time
        )

        self.__start_visualisation()

        self.c_logger.info("Successfully set the times into Json file.")

    def __set_time_picker(self, default_hours, default_mins):
        """
        Initialize a new Time Picker object.
        :param default_hours: Default hours of the new Time Picker object.
        :param default_mins: Default minutes of the new Time Picker object.
        :return: The created Time Picker object. Type: TimePicker
        """

        self.c_logger.info("Setting the time picker.")
        self.c_logger.info(
            "Default hours: {} , Default minutes: {}".format(default_hours, default_mins)
        )
        self.c_logger.info("Starting to create 'TimePicker' instance.")
        return_instance = TimePicker(self.main_window, str(default_hours), str(default_mins))
        self.c_logger.info("'TimePicker' instance has been created successfully.")
        return return_instance

    def __set_calendar(self, set_date=None):
        """
        Initialize and configure a new Date Entry object.
        :param set_date: If this parameter is provided then this value will be the default date of
                         the created Date Entry object. If it is not provided then the today date
                         will be set.
        :return: The created Date Entry object. Type: MyDateEntry
        """

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
        """
        Get the current value of the provided Data Entry.
        The required type: MyDateEntry
        :param calendar_instance: Instance of the Data Entry.
                                  Required type: MyDateEntry
        :return: The current value of the provided Data Entry
        """

        self.c_logger.info("Staring to get date from calendar.")
        self.c_logger.debug("The getting calendar instance: {}".format(calendar_instance))
        date_from_calendar = calendar_instance.get()
        self.c_logger.info("Successfully get the date from calendar.")
        self.c_logger.debug("The getting date from calendar: {}".format(date_from_calendar))
        return date_from_calendar

    def __get_time_from_time_picker(self, time_picker_instance):
        """
        Get the current value of the provided Time Picker.
        The required type: TimePicker
        :param time_picker_instance: Instance of the Time Picker.
                                     Required type: TimePicker
        :return: The current value of the provided Time Picker
        """

        self.c_logger.info("Staring to get time from time picker.")
        self.c_logger.debug("The getting time picker instance: {}".format(time_picker_instance))
        time_from_time_picker = time_picker_instance.get_time()
        if not time_from_time_picker:
            self.c_logger.error("The set time was not valid!")
        self.c_logger.info("Successfully get the time from time picker.")
        self.c_logger.debug("The getting time from time picker: {}".format(time_from_time_picker))
        return time_from_time_picker

    def plot(self):
        """
        This method integrates the created MatPlotLib Figure into the Main window.
        :return: None
        """

        self.c_logger.info("Starting to plot the figure onto TK canvas.")
        canvas = FigureCanvasTkAgg(self.plotterobj, master=self.main_window)
        self.c_logger.info("The figure has been plotted onto TK canvas successfully.")
        self.c_logger.debug("The 'FigureCanvasTkAgg' object: {}".format(canvas))
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, sticky="nsew")
        canvas.draw()
        self.c_logger.info("The complete figure has been integrated into GUI successfully.")


class UserConfigTab(object):
    """
    TODO: Fill this class with content.
    This tab contains all User configuration options.
    Planned options:
        - Name
        - Birth date
        - Employee number
        - Photo
    """


def main():
    window = tk.Tk()
    window.iconphoto(False, tk.PhotoImage(file=PATH_OF_WINDOW_ICON))
    window.title("Time reporting")
    # change ttk theme to 'clam' to fix issue with downarrow button
    style = ttk.Style(window)
    style.theme_use("alt")
    style.configure("BW.TLabel", foreground="black", background="white")
    style.configure(
        "C.TButton", font=("calibri", 12, "bold"), background="red",
    )
    note = ttk.Notebook(window)
    main_tab = tk.Frame(note)
    user_config_tab = tk.Frame(note)
    note.add(main_tab, text="Main")
    note.add(user_config_tab, text="User")
    note.pack()
    start = MainWindow(main_tab)
    window.protocol("WM_DELETE_WINDOW", start.quit_from_app)
    window.mainloop()


####
# ENTRY POINT
####


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--test",
        dest="test_flag",
        help="If this flag is set, the tool uses test values.",
        action="store_true",
    )

    args = parser.parse_args()

    test_run = args.test_flag

    main()
