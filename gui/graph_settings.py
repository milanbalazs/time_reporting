"""
This module contains all graph settings related implementations.
Eg.:
    - What should be visible on graph
    - What color should be used for elements
    - Date format
    - etc...
"""

import os
import sys
from tkinter import ttk
from tkinter import colorchooser

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

# Own modules imports
from color_logger import ColoredLogger


class GraphSettingsDataStorage(object):
    """
    This class contains the data of graph settings.
    """

    def __init__(self, graph_settings_config_parser):
        """
        Init method of the 'GraphSettingsDataStorage' class.
        :param graph_settings_config_parser: The configparser object of the related config file.
        """

        self.graph_settings_config_parser = graph_settings_config_parser

        # [COLORS]
        self.working_time_color = self.graph_settings_config_parser.get("COLORS", "working_time")
        self.break_time_color = self.graph_settings_config_parser.get("COLORS", "break_time")
        self.plus_time_color = self.graph_settings_config_parser.get("COLORS", "plus_time")
        self.minus_time_color = self.graph_settings_config_parser.get("COLORS", "minus_time")

        # [TIME_ELEMENTS]
        self.arriving_element = self.graph_settings_config_parser.getboolean(
            "TIME_ELEMENTS", "arriving"
        )
        self.leaving_element = self.graph_settings_config_parser.getboolean(
            "TIME_ELEMENTS", "leaving"
        )
        self.working_time_element = self.graph_settings_config_parser.getboolean(
            "TIME_ELEMENTS", "working_time"
        )
        self.plus_time_element = self.graph_settings_config_parser.getboolean(
            "TIME_ELEMENTS", "plus_time"
        )
        self.minus_time_element = self.graph_settings_config_parser.getboolean(
            "TIME_ELEMENTS", "minus_time"
        )

        # [DATE]
        self.format_date = self.graph_settings_config_parser.get("DATE", "format", raw=True)
        self.day_name_date = self.graph_settings_config_parser.getboolean("DATE", "day_name")

        # [OVERTIME]
        self.visible_overtime = self.graph_settings_config_parser.getboolean("OVERTIME", "visible")
        self.plus_time_overtime = self.graph_settings_config_parser.get("OVERTIME", "plus_time")
        self.minus_time_overtime = self.graph_settings_config_parser.get("OVERTIME", "minus_time")

        # [AXIS]
        self.x_axis_start = self.graph_settings_config_parser.get("AXIS", "x_axis_start", raw=True)
        self.x_axis_stop = self.graph_settings_config_parser.get("AXIS", "x_axis_stop", raw=True)
        self.x_axis_label = self.graph_settings_config_parser.get("AXIS", "x_axis_label")
        self.y_axis_label = self.graph_settings_config_parser.get("AXIS", "y_axis_label")
        self.overtime_y_axis_label = self.graph_settings_config_parser.get(
            "AXIS", "overtime_y_axis_label"
        )
        self.overtime_x_axis_label = self.graph_settings_config_parser.get(
            "AXIS", "overtime_x_axis_label"
        )


class GraphSettings(GraphSettingsDataStorage):
    """
    This class contains the all Graph Settings related attributes.
    """

    def __init__(self, main_window, c_logger=None, graph_settings_config_parser=None):
        """
        Init method of the 'GraphSettings' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param graph_settings_config_parser: The configparser object of the related config file.
        """

        super(GraphSettings, self).__init__(graph_settings_config_parser)
        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(self.main_window))
        self.graph_settings_config_parser = graph_settings_config_parser
        self._create_colors_gui_section()

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        :return: Instance of ColoredLogger
        """

        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "main_tab_log.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in graph_settings module.")

    def _create_colors_gui_section(self):
        color_config_label = ttk.Label(
            self.main_window, text="Colors", font=("Helvetica", 16, "bold")
        )
        color_config_label.grid(row=0, column=0, columnspan=2, sticky="s")

        self.working_time_color_button = tk.Button(
            self.main_window,
            text="Working-time",
            bg=self.working_time_color,
            command=lambda: self._get_selected_color(
                set_var="working_time_color",
                button=self.working_time_color_button,
                color=self.working_time_color,
            ),
        )
        self.working_time_color_button.grid(
            row=1, column=0, columnspan=2, sticky="n", padx=5, pady=5
        )

        self.break_time_color_button = tk.Button(
            self.main_window,
            text="Break",
            bg=self.break_time_color,
            command=lambda: self._get_selected_color(
                set_var="break_time_color",
                button=self.break_time_color_button,
                color=self.break_time_color,
            ),
        )
        self.break_time_color_button.grid(row=2, column=0, columnspan=2, sticky="n", padx=5, pady=5)

        self.plus_time_color_button = tk.Button(
            self.main_window,
            text="Plus-time",
            bg=self.plus_time_color,
            command=lambda: self._get_selected_color(
                set_var="plus_time_color",
                button=self.plus_time_color_button,
                color=self.plus_time_color,
            ),
        )
        self.plus_time_color_button.grid(row=3, column=0, columnspan=2, sticky="n", padx=5, pady=5)

        self.minus_time_color_button = tk.Button(
            self.main_window,
            text="Minus-time",
            bg=self.minus_time_color,
            command=lambda: self._get_selected_color(
                set_var="minus_time_color",
                button=self.minus_time_color_button,
                color=self.minus_time_color,
            ),
        )
        self.minus_time_color_button.grid(row=4, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def _get_selected_color(self, set_var=None, button=None, color=None):
        """
        Providing the selected color.
        :return: Selected color
        """

        color = colorchooser.askcolor(color=color)
        color_name = color[1]
        self.c_logger.info("Selected color: {}".format(color_name))
        if set_var:
            self.__setattr__(set_var, color_name)
        if button:
            button.configure(bg=color_name)
        return color_name