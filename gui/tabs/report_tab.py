"""
This module contains all report config related implementations.
It should mainly contain:
        - Date range
        - Formatting report
        - (print)
        - Export to:
            - PDF
            - Excel
            - CSV
            - HTML
            etc...
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
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "..", ".."))  # noqa: E402

# Own modules imports
from data_processor import DataProcessor
from color_logger import ColoredLogger
from date_entry import MyDateEntry
from file_type_picker import FileTypePicker


class ReportConfigTab(object):
    """
    TODO: Fill this class with content.
    This tab contains all report configuration related attributes.
    Planned options:
        - Date range
        - Formatting report
        - (print)
        - Export to:
            - PDF
            - Excel
            - CSV
            - HTML
    """

    def __init__(self, main_window, c_logger=None, data_processor=None):
        """
        Init method of the 'MainWindow' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param data_processor: Instance of DataProcessor module.
        """

        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))

        self.c_logger.info("Creating DataProcessor instance.")
        self.data_processor = (
            data_processor if data_processor else DataProcessor(c_logger=self.c_logger)
        )
        self.c_logger.info("DataProcessor instance successfully created.")

        self.__create_main_gui_section()

    def __set_default_report_dir(self):
        """
        Set the default directory to store the generated reports.
        :return: Path of the default directory.
        """

        self.c_logger.info("Start to set the default report directory.")
        default_report_dir = os.path.join(PATH_OF_FILE_DIR, "..", "..", "reports")
        self.c_logger.debug("The default report directory path: {}".format(default_report_dir))
        if not os.path.isdir(default_report_dir):
            self.c_logger.debug("The default report directory doesn't exist. Try to create it.")
            os.mkdir(default_report_dir)
        self.c_logger.debug("Star to norm the path")
        default_report_dir = os.path.normpath(default_report_dir)
        self.c_logger.debug("Formatted path: {}".format(default_report_dir))
        self.c_logger.info("The default report directory has been set successfully.")
        return default_report_dir

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

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        TODO: Make common method from it. It is used in more places.
        :return: Instance of ColoredLogger
        """

        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "report_tab_log.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in report_tab module.")

        return return_logger

    def __create_main_gui_section(self):
        """
        This method created the main gui section of Report generation.
        TODO: Split this method to smaller parts.
        TODO: Put the nested functions into upper level (class level)
        :return: None
        """

        report_generation_label = ttk.Label(
            self.main_window, text="Report Generation", font=("Helvetica", 16, "bold")
        )
        report_generation_label.grid(row=0, column=0, columnspan=3, sticky="s")

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=3, sticky="we"
        )

        report_generation_from_date = ttk.Label(self.main_window, text="From")
        report_generation_from_date.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        # Calculate the previous month to set the default 1 month visualisation.
        today = date.today()
        self.c_logger.info("Today: {}".format(today))
        previous_month = today - timedelta(days=30)
        self.c_logger.info("Previous 31 days: {}".format(previous_month))

        self.report_generation_from_calendar_instance = self.__set_calendar(set_date=previous_month)
        self.report_generation_from_calendar_instance.grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )

        report_generation_to_date = ttk.Label(self.main_window, text="To")
        report_generation_to_date.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.report_generation_to_calendar_instance = self.__set_calendar()
        self.report_generation_to_calendar_instance.grid(
            row=3, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=4, column=0, columnspan=3, sticky="we"
        )

        report_generation_file_type_label = ttk.Label(self.main_window, text="File type")
        report_generation_file_type_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)

        report_generation_file_name_label = ttk.Label(self.main_window, text="File name")
        report_generation_file_name_label.grid(row=6, column=0, sticky="e", padx=5, pady=5)

        # Get the entry content:
        # print(self.report_generation_file_name_entry.get())
        self.report_generation_file_name_entry = ttk.Entry(self.main_window, width=80)
        self.report_generation_file_name_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        def set_file_extension(event=None):
            self.report_generation_file_name_entry.delete(0, tk.END)
            self.report_generation_file_name_entry.insert(
                0, ".{}".format(self.file_type_picker.get_file_type().lower())
            )
            self.report_generation_file_name_entry.icursor(0)

        self.file_type_picker = FileTypePicker(
            self.main_window, ["PDF", "XML", "Json", "DAT", "XLSX"], command=set_file_extension
        )
        self.file_type_picker.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        set_file_extension()

        report_generation_file_location_label = ttk.Label(self.main_window, text="File directory")
        report_generation_file_location_label.grid(row=7, column=0, sticky="e", padx=5, pady=5)

        self.directory_entry_text = tk.StringVar(
            self.main_window, value=self.__set_default_report_dir()
        )

        self.report_generation_file_directory_entry = ttk.Entry(
            self.main_window, textvariable=self.directory_entry_text, width=80
        )
        self.report_generation_file_directory_entry.grid(
            row=7, column=1, sticky="w", padx=5, pady=5
        )

        def __browse_button():
            filename = tk.filedialog.askdirectory()
            self.directory_entry_text.set(filename)

        directory_browser_button = tk.Button(
            self.main_window, text="Browse", command=lambda: __browse_button(),
        )

        directory_browser_button.grid(row=7, column=2, sticky="w", padx=5, pady=5)

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=8, column=0, columnspan=3, sticky="we"
        )

        report_generation_start_button = tk.Button(
            self.main_window,
            text="Generate",
            font="Helvetica 10 bold",
            command=lambda: self.__start_report_generation(),
        )
        report_generation_start_button.grid(
            row=9, column=0, columnspan=3, sticky="n", padx=5, pady=5
        )

        self.__set_resizable(row=9, col=2)

        self.c_logger.info("The report generation GUI has been rendered successfully.")

    def __start_report_generation(self):
        """
        This method starts the report generation.
        TODO: Put functionality to this method.
        :return: None
        """

        self.c_logger.info("Start to generate the report.")

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
