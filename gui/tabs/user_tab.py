"""
This module contains all user config related implementations.
It should mainly contain:
        - Name
        - Birth date
        - Employee number
        - Photo
"""

import os
import sys
from tkinter import ttk

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

    def __init__(
        self, main_window, c_logger=None, user_info_parser=None, user_info_config_file_path=None
    ):
        """
        Init method of the 'MainWindow' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param user_info_parser: Instance of ConfigParser module (Parserd user info config file).
        :param user_info_config_file_path: Path of the used configuration file of user info.
        """

        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(main_window))
        self.user_info_parser = user_info_parser
        self.user_info_config_file_path = user_info_config_file_path

        self.__generate_complete_gui()

        self.__set_resizable(6, 1)

    def __generate_complete_gui(self):
        """
        Generating the complete User info related GUI parts.
        :return: None
        """

        self.__create_basic_user_info_gui_section()

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

    def __create_basic_user_info_gui_section(self):
        """
        Creating the basic user info GUI section.
        :return: None
        """

        self.c_logger.info("Starting to generate the main GUI section of report tab.")

        user_config_basic_label = ttk.Label(
            self.main_window, text="Basic user info", font=("Helvetica", 16, "bold")
        )
        user_config_basic_label.grid(row=0, column=0, columnspan=2, sticky="s")

        user_name_label = ttk.Label(self.main_window, text="Name")
        user_name_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        # Get the entry content:
        # print(self.user_name_entry.get())
        self.user_name_entry = ttk.Entry(self.main_window, width=80)
        self.user_name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.user_name_entry.insert(0, self.user_info_parser.get("BASIC_USER_INFO", "name"))

        user_id_label = ttk.Label(self.main_window, text="User ID")
        user_id_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.user_id_name_entry = ttk.Entry(self.main_window, width=80)
        self.user_id_name_entry.insert(0, self.user_info_parser.get("BASIC_USER_INFO", "user_id"))
        self.user_id_name_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        user_birth_label = ttk.Label(self.main_window, text="Birth date")
        user_birth_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.user_birth_name_entry = ttk.Entry(self.main_window, width=80)
        self.user_birth_name_entry.insert(
            0, self.user_info_parser.get("BASIC_USER_INFO", "birth_date")
        )
        self.user_birth_name_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        user_department_label = ttk.Label(self.main_window, text="Department")
        user_department_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)

        self.user_department_entry = ttk.Entry(self.main_window, width=80)
        self.user_department_entry.insert(
            0, self.user_info_parser.get("BASIC_USER_INFO", "department")
        )
        self.user_department_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        user_position_label = ttk.Label(self.main_window, text="Position")
        user_position_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)

        self.user_position_entry = ttk.Entry(self.main_window, width=80)
        self.user_position_entry.insert(0, self.user_info_parser.get("BASIC_USER_INFO", "position"))
        self.user_position_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        user_sap_label = ttk.Label(self.main_window, text="SAP ID")
        user_sap_label.grid(row=6, column=0, sticky="e", padx=5, pady=5)

        self.user_sap_entry = ttk.Entry(self.main_window, width=80)
        self.user_sap_entry.insert(0, self.user_info_parser.get("BASIC_USER_INFO", "sap_id"))
        self.user_sap_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        user_info_save_button = tk.Button(
            self.main_window,
            width=40,
            height=1,
            borderwidth=5,
            text="SAVE",
            font="Helvetica 14 bold",
            command=lambda: self.__user_info_save_callback(),
        )
        user_info_save_button.grid(row=7, column=0, columnspan=2, sticky="s", padx=5, pady=5)

    def __user_info_save_callback(self):
        """
        This method is the callback of the save button.
        :return: None
        """

        self.c_logger.info("Starting to call the save button callback.")

        self.user_info_parser.set("BASIC_USER_INFO", "name", self.user_name_entry.get())
        self.user_info_parser.set("BASIC_USER_INFO", "user_id", self.user_id_name_entry.get())
        self.user_info_parser.set("BASIC_USER_INFO", "birth_date", self.user_birth_name_entry.get())
        self.user_info_parser.set("BASIC_USER_INFO", "department", self.user_department_entry.get())
        self.user_info_parser.set("BASIC_USER_INFO", "position", self.user_position_entry.get())
        self.user_info_parser.set("BASIC_USER_INFO", "sap_id", self.user_sap_entry.get())

        with open(self.user_info_config_file_path, "w") as configfile:
            self.user_info_parser.write(configfile)

        self.__generate_complete_gui()

        self.c_logger.info("The save button callback was successful.")
