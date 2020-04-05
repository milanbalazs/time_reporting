"""
This module contains all main tab related implementations.
It should mainly contain:
    - Add new record
    - Modify existing record
    - Select date range
    - Visualise the:
        - Arriving time
        - Leaving time
        - Over time
"""

import matplotlib
import os
import sys
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from datetime import date, timedelta

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402
# Append the required directories to PATH
sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "..", ".."))  # noqa: E402

# Own modules imports
from data_processor import DataProcessor
from color_logger import ColoredLogger
from plotter3 import Plotter3
from time_picker import TimePicker
from date_entry import MyDateEntry
from graph_settings import GraphSettings

matplotlib.use("TkAgg")


class MainWindow(object):
    """
    This class contains the all Main Window related attributes.
    """

    def __init__(
        self,
        main_window,
        c_logger=None,
        data_processor=None,
        graph_settings=None,
        graph_settings_file_path=None,
    ):
        """
        Init method of the 'MainWindow' class.
        :param main_window: Instance of the main Tk window.
        :param graph_settings: Instance of the graph settings parser.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param data_processor: Instance of DataProcessor module.
        :param graph_settings_file_path: Path of the used graph settings config file.
        """

        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))

        self.c_logger.info("Creating DataProcessor instance.")
        self.data_processor = (
            data_processor if data_processor else DataProcessor(c_logger=self.c_logger)
        )
        self.c_logger.info("DataProcessor instance successfully created.")

        self.graph_settings_config_parser = graph_settings
        self.graph_settings_file_path = graph_settings_file_path

        self.graph_settings_top_level_window = None

        self.__create_new_record_gui_section()
        self.__create_visualisation_gui_section()

        self.__start_visualisation()

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        :return: Instance of ColoredLogger
        """

        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "main_tab_log.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in main_tab module.")

        return return_logger

    def __set_resizable(self, row, col):
        """
        The the rows and columns to be configurable (resizable).
        10 rows and 10 columns are set to resizable.
        TODO: Make common method from it. It is used in more places.
        :param: row: Number of configured rows.
        :param col: Number of configured columns.
        :return: None
        """

        self.c_logger.info("Starting to set the resizable rows and columns")
        for x in range(0, row + 1):
            self.c_logger.debug("Set the {}. row resizable.".format(x))
            self.main_window.grid_rowconfigure(x, weight=1)
        for x in range(0, col + 1):
            self.c_logger.debug("Set the {}. column resizable.".format(x))
            self.main_window.grid_columnconfigure(x, weight=1)
        self.c_logger.info("Successfully set the resizable rows and columns.")

    def __create_visualisation_gui_section(self):
        """
        Create the visualisation related GUI section and render it to the main window.
        TODO: Make common method from it. It is used in more places.
        :return: None
        """

        self.c_logger.info("Starting to create visualisation GUI section.")

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=6, column=0, columnspan=2, sticky="we"
        )

        visualisation_label = ttk.Label(
            self.main_window, text="Visualisation", font=("Helvetica", 16, "bold")
        )
        visualisation_label.grid(row=7, column=0, columnspan=2, sticky="s")

        visualisation_from_date = ttk.Label(self.main_window, text="From")
        visualisation_from_date.grid(row=8, column=0, sticky="e", padx=5, pady=5)

        # Calculate the previous month to set the default 1 month visualisation.
        today = date.today()
        self.c_logger.info("Today: {}".format(today))
        previous_month = today - timedelta(days=30)
        self.c_logger.info("Previous 31 days: {}".format(previous_month))

        self.visualisation_from_calendar_instance = self.__set_calendar(set_date=previous_month)
        self.visualisation_from_calendar_instance.grid(row=8, column=1, sticky="w", padx=5, pady=5)

        visualisation_to_date = ttk.Label(self.main_window, text="To")
        visualisation_to_date.grid(row=9, column=0, sticky="e", padx=5, pady=5)

        self.visualisation_to_calendar_instance = self.__set_calendar()
        self.visualisation_to_calendar_instance.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        settings_button = tk.Button(
            self.main_window, text="Settings", command=lambda: self.__graph_settings(),
        )
        settings_button.grid(row=10, column=0, columnspan=2, sticky="n", padx=5, pady=1)

        set_button = tk.Button(
            self.main_window,
            text="Start visualisation",
            command=lambda: self.__start_visualisation(),
        )
        set_button.grid(row=11, column=0, columnspan=2, sticky="n", padx=5, pady=1)

        self.__set_resizable(row=11, col=2)

        self.c_logger.info("Visualisation GUI section has been created successfully.")

    def __graph_settings(self):
        """
        This method handles the graph settings window.
        :return: None
        """

        if not self.graph_settings_top_level_window or not tk.Toplevel.winfo_exists(
            self.graph_settings_top_level_window
        ):
            self.c_logger.info("Starting to configure the graph")
            self.graph_settings_top_level_window = tk.Toplevel(self.main_window)
            self.graph_settings_top_level_window.title("Graph settings")
            GraphSettings(
                self.graph_settings_top_level_window,
                c_logger=self.c_logger,
                graph_settings_config_parser=self.graph_settings_config_parser,
                graph_settings_file_path=self.graph_settings_file_path,
            )

            self.graph_settings_top_level_window.bind("<Destroy>", self._top_level_closing_action)
        else:
            self.c_logger.warning("The Graph setting windows has been already opened!")

    def _top_level_closing_action(self, event):
        """
        This method handles if the top_level window has been closed.
        :return: None
        """

        if event.widget == event.widget.winfo_toplevel():

            self.c_logger.info("Start the top level window closing flow.")

            self.__start_visualisation()

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
            (
                arriving,
                leaving,
                break_time,
            ) = self.data_processor.get_arriving_leaving_break_times_based_on_date(single_date)
            if not arriving or not leaving:
                self.c_logger.warning(
                    "There is no arriving of leaving time for '()' date.".format(single_date)
                )
                arriving = "00:00"
                leaving = "00:00"
                break_time = "00:00"
            self.c_logger.info(
                "Date: {} ; Arriving: {} ; Leaving: {} ; Break: {}".format(
                    single_date, arriving, leaving, break_time
                )
            )

            plotting_list.append(
                {"date": single_date, "from": arriving, "to": leaving, "break": break_time}
            )
        self.c_logger.debug("Created plotting list: {}".format(plotting_list))
        self.c_logger.info("Starting to create 'Plotter3' instance.")
        self.plotter3 = Plotter3(
            plotting_list, c_logger=self.c_logger, graph_settings=self.graph_settings_config_parser
        )
        self.c_logger.info("'Plotter3' instance has been created successfully.")
        self.c_logger.info("Starting to get the figure object.")
        self.plotterobj = self.plotter3.plotting()
        self.c_logger.info("Geting figure: {}".format(self.plotterobj))
        self.c_logger.info("Starting to plot the figure to TK canvas.")
        self.plot()
        self.c_logger.info("The figure has been successfully plotted to TK canvas.")

    def set_available_data(self, event):
        """
        This method sets the time data for selected date (If it's available in data-set).
        This method is a call-back of Tk event.
        :param event: This method is a call-back of Tk event so this parameter is required.
        :return: None
        """

        self.c_logger.info(
            "Start to set the time date based on the selected date. "
            "It's an event triggered call back."
        )

        current_selected_date = self.__get_date_from_calendar(
            self.new_data_calendar_instance
        ).replace(" ", "")

        self.c_logger.debug("The selected date: {}".format(current_selected_date))

        (
            arriving,
            leaving,
            break_time,
        ) = self.data_processor.get_arriving_leaving_break_times_based_on_date(
            current_selected_date
        )

        self.c_logger.debug(
            "The times for the date: Arriving: {} ; Leaving: {} ; Break: {}".format(
                arriving, leaving, break_time
            )
        )

        if ("00:00", "00:00") == (arriving, leaving):
            self.c_logger.debug(
                "There is not data for {} date. " "Set default time.".format(current_selected_date)
            )
            # TODO: The hard-coded default time should come from the User config.
            self.arrive_time_picker_instance.set_time("09", "00")
            self.leaving_time_picker_instance.set_time("17", "20")
            self.break_time_picker_instance.set_time("00", "20")
            return

        arriving_h = arriving.split(":")[0]
        arriving_m = arriving.split(":")[1]

        leaving_h = leaving.split(":")[0]
        leaving_m = leaving.split(":")[1]

        break_time_h = break_time.split(":")[0]
        break_time_m = break_time.split(":")[1]

        self.c_logger.debug(
            "Hours: Arr: {} , Lea: {} , Br: {}; Mins: Arr: {} , Lea: {} , Br: {}".format(
                arriving_h, leaving_h, break_time_h, arriving_m, leaving_m, break_time_m
            )
        )

        self.arrive_time_picker_instance.set_time(arriving_h, arriving_m)
        self.leaving_time_picker_instance.set_time(leaving_h, leaving_m)
        self.break_time_picker_instance.set_time(break_time_h, break_time_m)

        self.c_logger.info("Successfully set the Arriving and Leaving times based on the date.")

    def __create_new_record_gui_section(self):
        """
        Create the visualisation related GUI section and render it to the main window.
        :return: None
        """

        self.c_logger.info("Starting to create the new record setting GUI section.")
        create_label = ttk.Label(
            self.main_window, text="Create record", font=("Helvetica", 16, "bold")
        )
        create_label.grid(row=0, column=0, columnspan=2, sticky="s")

        new_data_date_label = ttk.Label(self.main_window, text="Date")
        new_data_date_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.new_data_calendar_instance = self.__set_calendar()
        self.new_data_calendar_instance.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.new_data_calendar_instance.bind("<<DateEntrySelected>>", self.set_available_data)

        arrive_time_label = ttk.Label(self.main_window, text="Arriving")
        arrive_time_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.arrive_time_picker_instance = self.__set_time_picker("9", "0")
        self.arrive_time_picker_instance.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        leaving_time_label = ttk.Label(self.main_window, text="Leaving")
        leaving_time_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.leaving_time_picker_instance = self.__set_time_picker("17", "20")
        self.leaving_time_picker_instance.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        break_time_label = ttk.Label(self.main_window, text="Break")
        break_time_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)

        self.break_time_picker_instance = self.__set_time_picker("00", "20")
        self.break_time_picker_instance.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        set_button = tk.Button(
            self.main_window, text="Set record", command=lambda: self.__set_time_into_config_json(),
        )
        set_button.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)

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
        break_time = self.__get_time_from_time_picker(self.break_time_picker_instance)
        self.c_logger.info(
            "Current selected date: {} , Arriving: {} , Leaving: {}, Break: {}".format(
                current_selected_date, arriving_time, leaving_time, break_time
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
            messagebox.showerror("Wrong time range", error_msg)
            return
        self.c_logger.info("Starting to set the new record into Json file.")
        self.data_processor.set_time(
            current_selected_date.replace(" ", ""), arriving_time, leaving_time, break_time
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
        # The "rowspan" should be the same as number of used rows.
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=12, sticky="news")
        canvas.draw()
        self.c_logger.info("The complete figure has been integrated into GUI successfully.")
