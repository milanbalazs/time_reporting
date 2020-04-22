"""
This module contains all metrics related implementations.
It should mainly contain:
        - Number of working days
        - Number of weekend days
        - Required working hours
        - Number of working hours
        - Number of break hours
        - Number or over time hours (plus)
        - Number or over time hours (minus)
        - Number or over time hours (overall)
"""

import os
import sys
import datetime
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
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "..",))  # noqa: E402
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "..", ".."))  # noqa: E402

# Own modules imports
from data_processor import DataProcessor
from color_logger import ColoredLogger
from date_entry import MyDateEntry

LABEL_FONT = "Helvetica 14 bold"


class MetricsGetters(object):
    """
    This class contains all related getters for GUI.
    The GUI class should be inherited from this base class.
    """

    def __init__(self):
        pass


class MetricsTab(MetricsGetters):
    """
    This tab contains all Metrics related implementations.
    Planned options:
        - Number of working days
        - Number of weekend days
        - Required working hours
        - Number of working hours
        - Number of break hours
        - Number or over time hours (plus)
        - Number or over time hours (minus)
        - Number or over time hours (overall)
    """

    def __init__(
        self, main_window, c_logger=None, data_processor=None,
    ):
        """
        Init method of the 'MetricsTab' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param data_processor: Instance of DataProcessor module.
        """

        super(MetricsTab, self).__init__()

        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))
        self.c_logger.info("Creating DataProcessor instance.")
        self.data_processor = (
            data_processor if data_processor else DataProcessor(c_logger=self.c_logger)
        )
        self.c_logger.info("DataProcessor instance successfully created.")

        self.__generate_complete_gui()

    def __generate_complete_gui(self):
        """
        Generating the complete User info related GUI parts.
        :return: None
        """

        self.__create_date_selector_metrics_gui_section()
        self.__create_calculated_metrics_gui_section()

        self.__create_horizontal_separator_lines()

        self.__set_resizable(16, 1)

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

    def __create_horizontal_separator_lines(self):
        """
        This method creates the horizontal separator lines.
        :return: None
        """

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=4, sticky="we"
        )

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=6, column=0, columnspan=4, sticky="we"
        )

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

    def __create_date_selector_metrics_gui_section(self):
        """
        This method creates the date selector gui section of Metrics.
        :return: None
        """

        self.c_logger.info("Starting to generate the date selector GUI section of Metrics tab.")

        metrics_label = ttk.Label(self.main_window, text="Metrics", font=("Helvetica", 16, "bold"))
        metrics_label.grid(row=0, column=0, columnspan=2, sticky="s")

        metrics_date_selector_from_date = ttk.Label(self.main_window, text="From")
        metrics_date_selector_from_date.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        # Calculate the previous month to set the default 1 month visualisation.
        today = date.today()
        self.c_logger.info("Today: {}".format(today))
        previous_month = today - timedelta(days=30)
        self.c_logger.info("Previous 31 days: {}".format(previous_month))

        self.metrics_date_selector_from_calendar_instance = self.__set_calendar(
            set_date=previous_month
        )
        self.metrics_date_selector_from_calendar_instance.grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )

        metrics_selector_to_date = ttk.Label(self.main_window, text="To")
        metrics_selector_to_date.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.metrics_selector_to_calendar_instance = self.__set_calendar()
        self.metrics_selector_to_calendar_instance.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        metrics_start_button = tk.Button(
            self.main_window,
            width=20,
            height=1,
            borderwidth=3,
            text="Start",
            font=LABEL_FONT,
            command=lambda: self.__create_calculated_metrics_gui_section(),
        )
        metrics_start_button.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def __create_calculated_metrics_gui_section(self):
        """
        This method creates the calculated metrics gui section of Metrics.
        :return: None
        """

        self.c_logger.info(
            "Starting to generate the calculated metrics GUI section of Metrics tab."
        )

        week_days_label = ttk.Label(
            self.main_window, text="Week days: {}".format("666"), font=LABEL_FONT
        )
        week_days_label.grid(row=7, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        weekend_days_label = ttk.Label(
            self.main_window, text="Weekend days: {}".format("666"), font=LABEL_FONT
        )
        weekend_days_label.grid(row=8, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        worked_days_label = ttk.Label(
            self.main_window, text="Worked days: {}".format("666"), font=LABEL_FONT
        )
        worked_days_label.grid(row=9, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        missing_days_label = ttk.Label(
            self.main_window, text="Missing days: {}".format("666"), font=LABEL_FONT
        )
        missing_days_label.grid(row=10, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        required_working_hours_label = ttk.Label(
            self.main_window, text="Required working hours: {}".format("666"), font=LABEL_FONT
        )
        required_working_hours_label.grid(
            row=11, column=0, sticky="n", columnspan=2, padx=5, pady=5
        )

        working_hours_label = ttk.Label(
            self.main_window, text="Worked hours: {}".format("666"), font=LABEL_FONT
        )
        working_hours_label.grid(row=12, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        breaking_hours_label = ttk.Label(
            self.main_window, text="Break hours: {}".format("666"), font=LABEL_FONT
        )
        breaking_hours_label.grid(row=13, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        overtime_minus_hours_label = ttk.Label(
            self.main_window, text="Overtime minus: {}".format("666"), font=LABEL_FONT
        )
        overtime_minus_hours_label.grid(row=14, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        overtime_plus_hours_label = ttk.Label(
            self.main_window, text="Overtime plus: {}".format("666"), font=LABEL_FONT
        )
        overtime_plus_hours_label.grid(row=15, column=0, sticky="n", columnspan=2, padx=5, pady=5)

        overtime_overall_hours_label = ttk.Label(
            self.main_window, text="Overtime overall: {}".format("666"), font=LABEL_FONT
        )
        overtime_overall_hours_label.grid(
            row=16, column=0, sticky="n", columnspan=2, padx=5, pady=5
        )

    def __set_calendar(self, set_date=None):
        """
        Initialize and configure a new Date Entry object.
        TODO: Make common method from it. It is used in more places.
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
