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
        self.weekend_color = self.graph_settings_config_parser.get("COLORS", "weekend")

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

        # Helper variables
        self.entry_tk_vars = []


class GraphSettings(GraphSettingsDataStorage):
    """
    This class contains the all Graph Settings related attributes.
    """

    def __init__(
        self,
        main_window,
        c_logger=None,
        graph_settings_config_parser=None,
        graph_settings_file_path=None,
    ):
        """
        Init method of the 'GraphSettings' class.
        :param main_window: Instance of the main Tk window.
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is MAIN_LOGGER (Global variable.)
        :param graph_settings_config_parser: The configparser object of the related config file.
        :param graph_settings_file_path: Path of the used graph settings config file.
        """

        super(GraphSettings, self).__init__(graph_settings_config_parser)
        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.main_window = main_window
        self.c_logger.info("Get main window: {}".format(self.main_window))
        self.graph_settings_config_parser = graph_settings_config_parser
        self.graph_settings_file_path = graph_settings_file_path
        self._create_colors_gui_section()
        self._create_annotations_gui_section()
        self._create_date_gui_section()
        self._create_overtime_gui_section()
        self._create_axis_gui_section()
        self.save_and_cancel_button_gui()

        self.__create_horizontal_separator_lines()
        self.__create_vertical_separator_lines()

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

    def __create_vertical_separator_lines(self):
        """
        This method creates the vertical separator lines.
        :return: None
        """

        ttk.Separator(self.main_window, orient=tk.VERTICAL).grid(
            row=0, column=2, rowspan=6, sticky="ns"
        )

        ttk.Separator(self.main_window, orient=tk.VERTICAL).grid(
            row=0, column=5, rowspan=6, sticky="ns"
        )

        ttk.Separator(self.main_window, orient=tk.VERTICAL).grid(
            row=0, column=7, rowspan=6, sticky="ns"
        )

        ttk.Separator(self.main_window, orient=tk.VERTICAL).grid(
            row=0, column=10, rowspan=6, sticky="ns"
        )

    def __create_horizontal_separator_lines(self):
        """
        This method creates the horizontal separator lines.
        :return: None
        """

        ttk.Separator(self.main_window, orient=tk.HORIZONTAL).grid(
            row=6, column=0, columnspan=13, sticky="we"
        )

    def _create_colors_gui_section(self):
        """
        Creating the Color related gui section.
        :return: None
        """

        self.c_logger.info("Starting to create the color setting GUI section.")

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
                conf_section="COLORS",
                conf_option="working_time",
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
                conf_section="COLORS",
                conf_option="break_time",
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
                conf_section="COLORS",
                conf_option="plus_time",
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
                conf_section="COLORS",
                conf_option="minus_time",
            ),
        )
        self.minus_time_color_button.grid(row=4, column=0, columnspan=2, sticky="n", padx=5, pady=5)

        self.weekend_color_button = tk.Button(
            self.main_window,
            text="Weekends",
            bg=self.weekend_color,
            command=lambda: self._get_selected_color(
                set_var="weekend_color",
                button=self.weekend_color_button,
                color=self.weekend_color,
                conf_section="COLORS",
                conf_option="weekend",
            ),
        )
        self.weekend_color_button.grid(row=5, column=0, columnspan=2, sticky="n", padx=5, pady=5)

        self.c_logger.info("Color settings GUI section generation was successful.")

    def _create_annotations_gui_section(self):
        """
        Creating the Annotations related gui section.
        :return: None
        """

        self.c_logger.info("Starting to create the annotations setting GUI section.")

        annotation_config_label = ttk.Label(
            self.main_window, text="Annotations", font=("Helvetica", 16, "bold")
        )
        annotation_config_label.grid(row=0, column=3, columnspan=2, sticky="s")

        self.arriving_annotate_var = tk.IntVar()
        self.arriving_annotate_var.set(self.arriving_element)
        arriving_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Arriving",
            variable=self.arriving_annotate_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.arriving_annotate_var,
                conf_section="TIME_ELEMENTS",
                conf_option="arriving",
            ),
        )
        arriving_annotate_checkbox.grid(row=1, column=3)

        self.leaving_annotate_var = tk.IntVar()
        self.leaving_annotate_var.set(self.leaving_element)
        leaving_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Leaving",
            variable=self.leaving_annotate_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.leaving_annotate_var,
                conf_section="TIME_ELEMENTS",
                conf_option="leaving",
            ),
        )
        leaving_annotate_checkbox.grid(row=2, column=3)

        self.working_annotate_var = tk.IntVar()
        self.working_annotate_var.set(self.working_time_element)
        working_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Working-time",
            variable=self.working_annotate_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.working_annotate_var,
                conf_section="TIME_ELEMENTS",
                conf_option="working_time",
            ),
        )
        working_annotate_checkbox.grid(row=3, column=3)

        self.plus_annotate_var = tk.IntVar()
        self.plus_annotate_var.set(self.plus_time_element)
        plus_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Plus-time",
            variable=self.plus_annotate_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.plus_annotate_var,
                conf_section="TIME_ELEMENTS",
                conf_option="plus_time",
            ),
        )
        plus_annotate_checkbox.grid(row=4, column=3)

        self.minus_annotate_var = tk.IntVar()
        self.minus_annotate_var.set(self.minus_time_element)
        minus_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Minus-time",
            variable=self.minus_annotate_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.minus_annotate_var,
                conf_section="TIME_ELEMENTS",
                conf_option="minus_time",
            ),
        )
        minus_annotate_checkbox.grid(row=5, column=3)

        self.c_logger.info("Annotations settings GUI section generation was successful.")

    def _create_date_gui_section(self):
        """
        Creating the Date related gui section.
        :return: None
        """

        self.c_logger.info("Starting to create the date setting GUI section.")

        annotation_config_label = ttk.Label(
            self.main_window, text="Date", font=("Helvetica", 16, "bold")
        )
        annotation_config_label.grid(row=0, column=6, columnspan=2, sticky="s")

        self.day_name_date_var = tk.IntVar()
        self.day_name_date_var.set(self.minus_time_element)
        minus_annotate_checkbox = tk.Checkbutton(
            self.main_window,
            text="Day name",
            variable=self.day_name_date_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.day_name_date_var, conf_section="DATE", conf_option="day_name",
            ),
        )
        minus_annotate_checkbox.grid(row=1, column=6)

        self.date_format_picker_var = tk.StringVar()
        self.date_format_picker_var.set(self.format_date)

        # TODO: Extending the possible handled date formats.
        possible_formats = ["%Y.%m.%d."]

        self.date_format_picker_option = tk.OptionMenu(
            self.main_window,
            self.date_format_picker_var,
            *possible_formats,
            command=lambda _: self.set_date_format_picker_value(
                variable=self.date_format_picker_var, conf_section="DATE", conf_option="format"
            )
        )
        self.date_format_picker_option.grid(row=2, column=6, sticky="w", padx=5, pady=5)

        self.c_logger.info("Date settings GUI section generation was successful.")

    def _create_axis_gui_section(self):
        """
        Creating the Axises related gui section.
            [AXIS]
            x_axis_start = 05:00
            x_axis_stop = 21:00
            x_axis_label = Times
            y_axis_label = Dates
            overtime_y_axis_label = Times
            overtime_x_axis_label = Overtime
        :return: None
        """

        self.c_logger.info("Starting to create the axis setting GUI section.")

        axes_config_label = ttk.Label(
            self.main_window, text="Graph Axes", font=("Helvetica", 16, "bold")
        )
        axes_config_label.grid(row=0, column=11, columnspan=2, sticky="s")

        x_axis_start_label = tk.Label(self.main_window, text="X axis start")
        x_axis_start_label.grid(row=1, column=11, sticky="e")
        x_axis_start_var = tk.StringVar()
        x_axis_start_var.set(self.x_axis_start)
        self.entry_tk_vars.append([x_axis_start_var, "AXIS", "x_axis_start"])
        x_axis_start_entry = tk.Entry(self.main_window, bd=5, textvariable=x_axis_start_var)
        x_axis_start_entry.grid(row=1, column=12, sticky="w")

        x_axis_stop_label = tk.Label(self.main_window, text="X axis stop")
        x_axis_stop_label.grid(row=2, column=11, sticky="e")
        x_axis_stop_var = tk.StringVar()
        x_axis_stop_var.set(self.x_axis_stop)
        self.entry_tk_vars.append([x_axis_stop_var, "AXIS", "x_axis_stop"])
        x_axis_stop_entry = tk.Entry(self.main_window, bd=5, textvariable=x_axis_stop_var)
        x_axis_stop_entry.grid(row=2, column=12, sticky="w")

        x_axis_label_label = tk.Label(self.main_window, text="X axis label")
        x_axis_label_label.grid(row=3, column=11, sticky="e")
        x_axis_label_var = tk.StringVar()
        x_axis_label_var.set(self.x_axis_label)
        self.entry_tk_vars.append([x_axis_label_var, "AXIS", "x_axis_label"])
        x_axis_label_entry = tk.Entry(self.main_window, bd=5, textvariable=x_axis_label_var)
        x_axis_label_entry.grid(row=3, column=12, sticky="w")

        y_axis_label_label = tk.Label(self.main_window, text="Y axis label")
        y_axis_label_label.grid(row=4, column=11, sticky="e")
        y_axis_label_var = tk.StringVar()
        y_axis_label_var.set(self.y_axis_label)
        self.entry_tk_vars.append([y_axis_label_var, "AXIS", "y_axis_label"])
        y_axis_label_entry = tk.Entry(self.main_window, bd=5, textvariable=y_axis_label_var)
        y_axis_label_entry.grid(row=4, column=12, sticky="w")

    def _create_overtime_gui_section(self):
        """
        Creating the Overtime related gui section.
        :return: None
        """

        self.c_logger.info("Starting to create the overtime setting GUI section.")

        annotation_config_label = ttk.Label(
            self.main_window, text="Overtime", font=("Helvetica", 16, "bold")
        )
        annotation_config_label.grid(row=0, column=8, columnspan=2, sticky="s")

        self.over_time_graph_visible_var = tk.IntVar()
        self.over_time_graph_visible_var.set(self.visible_overtime)
        over_time_graph_visible_checkbox = tk.Checkbutton(
            self.main_window,
            text="Visible",
            variable=self.over_time_graph_visible_var,
            command=lambda: self.set_checkbutton_value(
                variable=self.over_time_graph_visible_var,
                conf_section="OVERTIME",
                conf_option="visible",
            ),
        )
        over_time_graph_visible_checkbox.grid(row=1, column=8, columnspan=2)

        self.over_time_minus_color_button = tk.Button(
            self.main_window,
            text="Minus overtime",
            bg=self.minus_time_overtime,
            command=lambda: self._get_selected_color(
                set_var="minus_time_overtime",
                button=self.over_time_minus_color_button,
                color=self.minus_time_overtime,
                conf_section="OVERTIME",
                conf_option="minus_time",
            ),
        )
        self.over_time_minus_color_button.grid(
            row=2, column=8, columnspan=2, sticky="n", padx=5, pady=5
        )

        self.over_time_plus_color_button = tk.Button(
            self.main_window,
            text="Plus overtime",
            bg=self.plus_time_overtime,
            command=lambda: self._get_selected_color(
                set_var="plus_time_overtime",
                button=self.over_time_plus_color_button,
                color=self.plus_time_overtime,
                conf_section="OVERTIME",
                conf_option="plus_time",
            ),
        )
        self.over_time_plus_color_button.grid(
            row=3, column=8, columnspan=2, sticky="n", padx=5, pady=5
        )

        x_axis_label_label = tk.Label(self.main_window, text="X axis label")
        x_axis_label_label.grid(row=4, column=8, sticky="e")
        x_axis_label_var = tk.StringVar()
        x_axis_label_var.set(self.overtime_x_axis_label)
        self.entry_tk_vars.append([x_axis_label_var, "AXIS", "overtime_x_axis_label"])
        x_axis_label_entry = tk.Entry(self.main_window, bd=5, textvariable=x_axis_label_var)
        x_axis_label_entry.grid(row=4, column=9, sticky="w")

        y_axis_label_label = tk.Label(self.main_window, text="Y axis label")
        y_axis_label_label.grid(row=5, column=8, sticky="e")
        y_axis_label_var = tk.StringVar()
        y_axis_label_var.set(self.overtime_y_axis_label)
        self.entry_tk_vars.append([y_axis_label_var, "AXIS", "overtime_y_axis_label"])
        y_axis_label_entry = tk.Entry(self.main_window, bd=5, textvariable=y_axis_label_var)
        y_axis_label_entry.grid(row=5, column=9, sticky="w")

        self.c_logger.info("Overtime settings GUI section generation was successful.")

    def _update_entry_tk_vars(self):
        """
        Update the textvariables of tk.Entry fields.
        :return: None
        """

        self.c_logger.info("Starting to update the textvariables of tk.Entry widgets")

        for single_var in self.entry_tk_vars:
            value_of_tk_var = single_var[0].get()
            if value_of_tk_var != self.graph_settings_config_parser.get(
                single_var[1], single_var[2]
            ):
                self.graph_settings_config_parser.set(
                    single_var[1], single_var[2], value_of_tk_var,
                )

        self.c_logger.info("textvariables of tk.Entry widgets have been updated successfully")

    def set_date_format_picker_value(self, variable=None, conf_section=None, conf_option=None):
        """
        This is a callback of date format picker.
        If a date picker changes this callback updates the configparser object.
        :param variable: The reference of the related variable.
        :param conf_section: Related section in the config file.
        :param conf_option: Related options in the config file.
        :return: None
        """

        self.c_logger.info("Update the date format picker variable in config file.")
        self.c_logger.debug(
            "Getting values: Variable: {} ; Section: {} ; Option: {}".format(
                variable, conf_section, conf_option
            )
        )
        self.c_logger.debug("Variable value: {}".format(variable.get()))

        if conf_section and conf_option:
            # TODO: The '%' character usage should be fixed in date format.
            #  https://stackoverflow.com/questions/14340366/configparser-and-string-with
            self.graph_settings_config_parser.set(
                conf_section, conf_option, variable.get(),
            )
            return
        self.c_logger.warning(
            "The section of option parameter hasn't got. "
            "The config file won't be updated with the new value."
        )

    def set_entry_value(self, variable, conf_section=None, conf_option=None):
        """
        This is a callback of tk.Entry.
        If a checkbutton changes this callback updates the configparser object.
        :param variable: The reference of the related variable.
        :param conf_section: Related section in the config file.
        :param conf_option: Related options in the config file.
        :return: None
        """

        self.c_logger.info("Update the checkbutton variable in config file.")
        self.c_logger.debug(
            "Getting values: Variable: {} ; Section: {} ; Option: {}".format(
                variable, conf_section, conf_option
            )
        )
        self.c_logger.debug("Variable value: {}".format(variable.get()))

        if conf_section and conf_option:
            self.graph_settings_config_parser.set(
                conf_section, conf_option, "True" if variable.get() else "False"
            )
            return
        self.c_logger.warning(
            "The section of option parameter hasn't got. "
            "The config file won't be updated with the new value."
        )

    def set_checkbutton_value(self, variable, conf_section=None, conf_option=None):
        """
        This is a callback of check buttons.
        If a checkbutton changes this callback updates the configparser object.
        :param variable: The reference of the related variable.
        :param conf_section: Related section in the config file.
        :param conf_option: Related options in the config file.
        :return: None
        """

        self.c_logger.info("Update the checkbutton variable in config file.")
        self.c_logger.debug(
            "Getting values: Variable: {} ; Section: {} ; Option: {}".format(
                variable, conf_section, conf_option
            )
        )
        self.c_logger.debug("Variable value: {}".format(variable.get()))

        if conf_section and conf_option:
            self.graph_settings_config_parser.set(
                conf_section, conf_option, "True" if variable.get() else "False"
            )
            return
        self.c_logger.warning(
            "The section of option parameter hasn't got. "
            "The config file won't be updated with the new value."
        )

    def save_and_cancel_button_gui(self):
        """
        This method handles the save/cancel button functionality.
        :return: None
        """

        self.c_logger.info("Starting to generate the Save and Cancel buttons.")

        save_button = tk.Button(self.main_window, text="Save", command=self.update_config_file,)
        save_button.grid(row=7, column=0, columnspan=13, sticky="n", padx=5, pady=5)

        cancel_button = tk.Button(self.main_window, text="Cancel", command=self._quit_top_level,)
        cancel_button.grid(row=8, column=0, columnspan=13, sticky="n", padx=5, pady=5)

        self.c_logger.info("The 'Save' and 'Cancel' button has been generated successfully.")

    def update_config_file(self):
        """
        This method update the related INI config file with the changed values.
        :return: None
        """

        self.c_logger.info("Starting to update the config file with the new values.")

        self._update_entry_tk_vars()

        with open(self.graph_settings_file_path, "w") as configfile:
            self.graph_settings_config_parser.write(configfile)

        self.c_logger.info("Config updating was successful. Destroying the top level GUI.")

        self._quit_top_level()

    def _quit_top_level(self):
        """
        Quit from this top level GUI.
        :return: None
        """

        self.c_logger.info("Starting to destroy the top level GUI.")

        self.main_window.destroy()

    def _get_selected_color(
        self, set_var=None, button=None, color=None, conf_section=None, conf_option=None
    ):
        """
        Providing the selected color.
        :param set_var: Name of the variable in the data class.
        :param button: Reference of the related button.
        :param color: The current color of the element.
                      This color will be the default of the color chooser.
        :param conf_section: Related section in the config file.
        :param conf_option: Related options in the config file.
        :return: Selected color
        """

        self.c_logger.info("Starting to get the selected color.")
        self.c_logger.debug(
            "Getting parameters: set_var: {}, button: {}, "
            "color: {}, section: {}, option: {}".format(
                set_var, button, color, conf_section, conf_option
            )
        )

        self.main_window.attributes("-topmost", 0)

        color = colorchooser.askcolor(color=color)
        color_name = color[1]

        self.main_window.attributes("-topmost", 1)

        self.c_logger.info("Selected color: {}".format(color_name))
        if set_var:
            self.__setattr__(set_var, color_name)
        if button:
            button.configure(bg=color_name)
        if conf_section and conf_option:
            self.graph_settings_config_parser.set(conf_section, conf_option, color_name)
        else:
            self.c_logger.warning(
                "The section of option parameter hasn't got. "
                "The config file won't be updated with the new value."
            )
        return color_name
