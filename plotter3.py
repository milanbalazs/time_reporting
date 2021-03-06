"""
This module contains the all plotting related implementations.
Two subplots are created in this module:
    - The main figure which contains the Date/Time data
    - The overtime figure which contains the plus or minus horus in the data range.
"""

# Import built-in modules

import matplotlib.pyplot as plt
import os
import sys
import json
import datetime

# Own modules imports

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402

sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "tools"))  # noqa: E402

from helper_functions import x_axis_data_generator
from helper_functions import X_AXIS_CONFIG_FILE_PATH
from color_logger import ColoredLogger

# Format of the time. Hours:Minutes
FMT = "%H:%M"


class Plotter3(object):
    """
    This class contains the all plotting related attributes.
    """

    def __init__(self, plot_data, c_logger=None, graph_settings=None):
        """
        Init method of the 'Plotter3' class.
        :param plot_data: Data for the plotting.
                          Required structure:
                          [
                            {
                                'date': '2020.02.09.',
                                'from': '00:00',
                                'to': '00:00'
                            },
                            {
                                'date': '2020.02.10.',
                                'from': '06:10',
                                'to': '18:25'
                            }
                          ]
        :param c_logger: Logger instance (ColoredLogger type is recommended).
                         Default is DEFAULT_LOGGER (Global variable.)
        :param graph_settings:  Instance of the graph settings parser.
                                It contains the custom graph parameters.
        """

        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()

        self.graph_settings = graph_settings

        self.c_logger.debug("Getting plot data: {}".format(plot_data))

        self.plot_data = plot_data

        self.c_logger.info("Starting to get X axis config data.")
        self.x_axis_config_data = self.__get_x_axis_config_data()
        self.c_logger.debug("X axis config data:\n{}".format(self.x_axis_config_data))
        self.c_logger.info("X axis config data has been successfully got.")

        x_axis_start_val = self.x_axis_config_data[self.graph_settings.get("AXIS", "x_axis_start")]
        x_axis_start_val = (
            x_axis_start_val
            if x_axis_start_val % 50 == 0
            else x_axis_start_val - (x_axis_start_val % 50)
        )
        x_axis_stop_val = self.x_axis_config_data[self.graph_settings.get("AXIS", "x_axis_stop")]
        x_axis_stop_val = (
            x_axis_stop_val
            if x_axis_stop_val % 50 == 0
            else x_axis_stop_val + 50 - x_axis_stop_val % 50
        )

        self.c_logger.info("Starting to calculate X axis tick labels.")
        # Example of generated X axis tick labels:
        # ['05:00', '06:40', '08:20', '10:00', '11:40', '13:20', '15:00', '16:40', '18:20', '20:00']
        self.x_axis_tick_labels = [
            x
            for idx, x in enumerate(self.x_axis_config_data.keys())
            if x_axis_start_val <= idx <= x_axis_stop_val and idx % 50 == 0
        ]
        self.c_logger.debug("X axis tick labels:\n{}".format(self.x_axis_tick_labels))
        self.c_logger.info("X axis tick labels has been successfully calculated.")

        self.c_logger.info("Starting to calculate X axis ticks.")
        # Example of generated X axis ticks:
        # [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
        self.x_axis_ticks = [
            idx
            for idx, x in enumerate(self.x_axis_config_data.keys())
            if x_axis_start_val <= idx <= x_axis_stop_val and idx % 50 == 0
        ]
        self.c_logger.debug("X axis ticks:\n{}".format(self.x_axis_ticks))
        self.c_logger.info("X axis ticks has been successfully calculated.")

        self.x_axis_limit = len(
            [
                x
                for idx, x in enumerate(self.x_axis_config_data.keys())
                if x_axis_start_val <= idx <= x_axis_stop_val
            ]
        )
        self.c_logger.info("X axis limit: {}".format(self.x_axis_limit))

        self.c_logger.info("Starting to calculate Y axis ticks.")
        self.y_axis_ticks = [x * 3 for x in range(len(plot_data) + 1) if x]
        self.c_logger.debug("Y axis ticks:\n".format(self.y_axis_ticks))
        self.c_logger.info("Y axis ticks has been successfully calculated.")

        self.y_axis_limit = (len(plot_data) + 1) * 3
        self.c_logger.info("Y axis limit: {}".format(self.y_axis_limit))

        self.dates = []
        self.c_logger.info("Starting to extract the getting plot data list.")
        for single_dict in plot_data:
            self.c_logger.debug("Get single dict: {}".format(single_dict))
            for key, value in single_dict.items():
                self.c_logger.debug("Key: {} , Value: {}".format(key, value))
                if key == "date":
                    self.c_logger.debug("'{}' value append to dates list.".format(value))
                    self.dates.append(value)
        self.c_logger.info("The getting plot data list has been successfully processed.")

        self.c_logger.info("Starting to create plottable dict.")
        self.plotable_dict = self.create_plottable_dict()
        self.c_logger.info("Plottable dict has been created successfully.")

        if not self.graph_settings.getboolean("OVERTIME", "visible"):
            self.fig, self.axis_array = plt.subplots(figsize=(10, 8))
            self.axis_array = [self.axis_array]
        else:
            self.fig, self.axis_array = plt.subplots(
                1, 2, figsize=(12, 8), gridspec_kw={"width_ratios": [8, 1]}
            )

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        :return: Instance of ColoredLogger
        """

        # Set-up a default logger if it is not provided by another module.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "logs", "plotter.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in main_tab module.")

        return return_logger

    def __get_x_axis_config_data(self):
        """
        Get the X axis data from config file.
        The used config file: conf/x_axis_config.json
        :return: The X axis data in a dict.
                 Structure: {"00:00": 0, "00:01": 1, "00:02": 2, "00:03": 3, ...}
        """

        self.c_logger.info("Starting to get the X axis data from config file.")
        self.c_logger.info("The used config file: {}".format(X_AXIS_CONFIG_FILE_PATH))
        if not os.path.isfile(X_AXIS_CONFIG_FILE_PATH):
            self.c_logger.warning(
                "'{}' file doesn't not exist. Call the generator method.".format(
                    X_AXIS_CONFIG_FILE_PATH
                )
            )
            # If the config file doesn't exist, the generator creates one.
            # It comes from helper_functions module.
            x_axis_data_generator(
                self.graph_settings.get("AXIS", "x_axis_start"),
                self.graph_settings.get("AXIS", "x_axis_stop"),
            )
            self.c_logger.info("X axis data config generator method has been successfully called.")
        self.c_logger.info("Starting to open the '{}' config file.".format(X_AXIS_CONFIG_FILE_PATH))
        with open(X_AXIS_CONFIG_FILE_PATH, "r") as opened_json:
            return_x_axis_config_data = json.load(opened_json)
        self.c_logger.debug(
            "The X axis data from config file:\n{}".format(return_x_axis_config_data)
        )
        self.c_logger.info("The X axis data from the config file has been successfully parsed.")
        return return_x_axis_config_data

    def get_effective_hours_decreased_with_break(self, time_data):
        """
        This method provides the Effective hours which is decreased by break time.
        :param time_data: The data structure which contains the time data.
                    Required data structure:
                        [
                            {
                                "date": "2020.03.30.",
                                "from": "09:00",
                                "to": "17:20",
                                "break": "00:20"}
                            },
                            ...
                            ...
                        ]
        :return:
        """

        pass

    @staticmethod
    def get_required_working_hours(time_data):
        """
        This method provides the Effective hours which is decreased by break time.
        :param time_data: The data structure which contains the time data.
                    Required data structure:
                        [
                            {
                                "date": "2020.03.30.",
                                "from": "09:00",
                                "to": "17:20",
                                "break": "00:20"}
                            },
                            ...
                            ...
                        ]
        :return:
        """

        required_working_time = datetime.datetime.strptime(
            time_data["break"], FMT
        ) + datetime.timedelta(hours=8)

        required_working_time = "{:02d}:{:02d}".format(
            int(required_working_time.hour), int(required_working_time.minute)
        )

        return required_working_time

    def is_weekend(self, date):
        """
        This method provides the weekdays.
        :param date: The ralated date.
        :return: ?
        """

        self.c_logger.debug("Starint to check if the date is weekend.")

        dt = datetime.datetime.strptime(date, "%Y.%m.%d.")

        self.c_logger.debug(
            "String date: {} ; DateTime: {} ; Day value: {}".format(date, dt, dt.weekday())
        )

        if dt.weekday() in (5, 6):
            self.c_logger.debug("{} - Weekend".format(date))
            return True
        else:
            self.c_logger.debug("{} - Weekday".format(date))
            return False

    def create_plottable_dict(self):
        """
        Creates a dictionary which contains the numbers instead of strings.
        This dictionary is generated by conf/x_axis_config.json config file.
        This dictionary is used to:
            - Plot the bars on the graph (X axes coordinates).
            - Create the annotates on the bars (Arriving/Leaving/Overtime/Working-hours).
        :return: A dictionary which contains the all data for plotting.
                 Structure:
                 [{'from': 0, 'to': 0, 'minus': 480, 'plus': None,
                   'plus_minus_human_readable': '-08:00', 'working_hours_human_readable': '00:00',
                   'from_hours_human_readable': '00:00', 'to_hours_human_readable': '00:00'}, ...]
        """

        # TODO: Split this method to more smaller and more readable/understandable format.

        self.c_logger.info("Starting to create the plottable dict.")
        return_times = []
        self.c_logger.info("Starting to get the elements from plotting data one by one.")
        for single_dict in self.plot_data:

            self.c_logger.debug("Single dict from plot data: {}".format(single_dict))

            if single_dict["from"] == "00:00" and single_dict["to"] == "00:00":
                self.c_logger.debug("No real data for {} date".format(single_dict["date"]))
                return_times.append(
                    {
                        "from": 0,
                        "to": 0,
                        "minus": 480,
                        "plus": None,
                        "break": 0,
                        "weekend": self.is_weekend(single_dict["date"]),
                        "plus_minus_human_readable": "00:00",
                        "working_hours_human_readable": "00:00",
                        "from_hours_human_readable": "00:00",
                        "to_hours_human_readable": "00:00",
                    }
                )
                continue

            time_delta = datetime.datetime.strptime(
                single_dict["to"], FMT
            ) - datetime.datetime.strptime(single_dict["from"], FMT)

            self.c_logger.debug("Calculated time delta: {}".format(time_delta))

            # IF YOU HAVE PLUS TIME
            ellapsed_hours = int(divmod(time_delta.total_seconds(), 3600)[0])
            ellapsed_mins = int(divmod(time_delta.total_seconds(), 60)[0]) - (ellapsed_hours * 60)
            time_in_office = "{:02d}:{:02d}".format(int(ellapsed_hours), int(ellapsed_mins))

            required_working_time = self.get_required_working_hours(single_dict)
            self.c_logger.debug("Required working time: {}".format(required_working_time))

            effective_hours_delta = datetime.datetime.strptime(
                time_in_office, FMT
            ) - datetime.datetime.strptime(required_working_time, FMT)

            self.c_logger.debug(
                (
                    "Elapsed hours: {} , Elapsed minutes: {} , "
                    "Time in office: {} , Effective hours delta: {}"
                ).format(ellapsed_hours, ellapsed_mins, time_in_office, effective_hours_delta)
            )

            ellapsed_hours = int(divmod(effective_hours_delta.total_seconds(), 3600)[0])
            ellapsed_mins = int(divmod(effective_hours_delta.total_seconds(), 60)[0]) - (
                ellapsed_hours * 60
            )

            plus_or_minus_time = "{:02d}:{:02d}".format(int(ellapsed_hours), int(ellapsed_mins))

            self.c_logger.debug(
                "Elapsed hours: {} , Elapsed minutes: {} , "
                "Plus or minus time: {}".format(ellapsed_hours, ellapsed_mins, plus_or_minus_time)
            )

            # IF YOU HAVE MINUS TIME

            if effective_hours_delta.days < 0:
                self.c_logger.debug("You have minus time")
                effective_hours_delta = datetime.datetime.strptime(
                    required_working_time, FMT
                ) - datetime.datetime.strptime(time_in_office, FMT)

                ellapsed_hours = int(divmod(effective_hours_delta.total_seconds(), 3600)[0])
                ellapsed_mins = int(divmod(effective_hours_delta.total_seconds(), 60)[0]) - (
                    ellapsed_hours * 60
                )

                plus_or_minus_time = "-{:02d}:{:02d}".format(
                    abs(int(ellapsed_hours)), int(ellapsed_mins)
                )

                self.c_logger.debug(
                    (
                        "Effective hours delta: {} , Elapsed hours: {} , Elapsed minutes: {} , "
                        "Plus or minus time: {}"
                    ).format(
                        effective_hours_delta, ellapsed_hours, ellapsed_mins, plus_or_minus_time
                    )
                )

            time_offset = self.x_axis_config_data[single_dict["to"]]

            self.c_logger.debug("Time offset: {}".format(time_offset))

            break_time = self.x_axis_config_data[single_dict["break"]]

            # TODO: The following if-else almost code duplication. Should be refactored!
            if "-" in plus_or_minus_time:
                self.c_logger.debug("'-' character is in Plus/Minus time.")
                minus_time = self.x_axis_config_data[plus_or_minus_time.replace("-", "")]
                self.c_logger.debug("Minus time without offset: {}".format(minus_time))
                minus_time += time_offset
                self.c_logger.debug("Minus time with offset: {}".format(minus_time))
                return_times.append(
                    {
                        "from": self.x_axis_config_data[single_dict["from"]],
                        "to": self.x_axis_config_data[single_dict["to"]],
                        "minus": minus_time,
                        "plus": None,
                        "break": break_time,
                        "weekend": self.is_weekend(single_dict["date"]),
                        "plus_minus_human_readable": plus_or_minus_time,
                        "working_hours_human_readable": time_in_office,
                        "from_hours_human_readable": single_dict["from"],
                        "to_hours_human_readable": single_dict["to"],
                    }
                )
            else:
                self.c_logger.debug("'-' character is NOT in Plus/Minus time.")
                plus_time = self.x_axis_config_data[plus_or_minus_time]
                self.c_logger.debug("Plus time: {}".format(plus_time))
                return_times.append(
                    {
                        "from": self.x_axis_config_data[single_dict["from"]],
                        "to": self.x_axis_config_data[single_dict["to"]] - plus_time,
                        "minus": None,
                        "plus": plus_time,
                        "break": break_time,
                        "weekend": self.is_weekend(single_dict["date"]),
                        "plus_minus_human_readable": "+{}".format(plus_or_minus_time),
                        "working_hours_human_readable": time_in_office,
                        "from_hours_human_readable": single_dict["from"],
                        "to_hours_human_readable": single_dict["to"],
                    }
                )
        self.c_logger.debug("Return data structure:\n{}".format(return_times))
        self.c_logger.info("Plottable data generation has been successfully generated.")
        return return_times

    def create_annotate(self, instance, y_position, data):
        """
        Create the annotates for the bars on the graph.
        Created annotates:
            - Arriving time
            - Leaving time
            - Overtime (plus/minus)
            - Working hours
        :param instance: Instance of axes.
        :param y_position: Current Y position (the graph which row in is).
        :param data: Dictionary which contains the coordinates and human readable times.
                     Data Structure:
                     [{'from': 0, 'to': 0, 'minus': 480, 'plus': None,
                     'plus_minus_human_readable': '-08:00', 'working_hours_human_readable': '00:00',
                     'from_hours_human_readable': '00:00', 'to_hours_human_readable': '00:00'}, ...]
        :return: None
        """

        self.c_logger.info("Starting to create annotates.")
        self.c_logger.debug(
            "Instance: {} , Y position: {} , Data: {}".format(instance, y_position, data)
        )
        if data["minus"]:
            if self.graph_settings.getboolean("TIME_ELEMENTS", "minus_time"):
                instance.annotate(data["plus_minus_human_readable"], xy=(data["minus"], y_position))
            if self.graph_settings.getboolean("TIME_ELEMENTS", "leaving"):
                instance.annotate(
                    data["to_hours_human_readable"], xy=(data["to"] - 55, y_position),
                )
        else:
            if self.graph_settings.getboolean("TIME_ELEMENTS", "plus_time"):
                instance.annotate(
                    data["plus_minus_human_readable"], xy=(data["to"] + data["plus"], y_position),
                )
            if self.graph_settings.getboolean("TIME_ELEMENTS", "leaving"):
                instance.annotate(
                    data["to_hours_human_readable"],
                    xy=(data["to"] + data["plus"] - 60, y_position),
                )

        if self.graph_settings.getboolean("TIME_ELEMENTS", "working_time"):
            instance.annotate(
                data["working_hours_human_readable"], xy=(data["from"] - 60, y_position),
            )

        if self.graph_settings.getboolean("TIME_ELEMENTS", "arriving"):
            instance.annotate(
                data["from_hours_human_readable"], xy=(data["from"], y_position),
            )
        self.c_logger.info("Annotates have been created successfully.")

    def overtime_graph_plotting(self):
        """
        This method plots the overtime (plus/minus).
        :return: None
        """

        # TODO: Split this method more smaller and more understandable/readable methods.

        self.c_logger.info("Starting to plot the overtime hours in the data range.")

        over_time_seconds = 0
        for single_dict in self.plotable_dict:
            if single_dict["minus"]:
                if single_dict["minus"] == 480:
                    self.c_logger.debug("Off day")
                    continue
                self.c_logger.debug(
                    "Minus time!\nFrom: {} , To: {} , Minus: {} , Working hours: {}".format(
                        single_dict["from_hours_human_readable"],
                        single_dict["to_hours_human_readable"],
                        single_dict["plus_minus_human_readable"],
                        single_dict["working_hours_human_readable"],
                    )
                )

                over_time = datetime.datetime.strptime("00:00", FMT) - datetime.datetime.strptime(
                    single_dict["plus_minus_human_readable"].replace("-", ""), FMT
                )
                over_time_seconds += over_time.total_seconds()
                self.c_logger.debug("Overtime is secs: {}".format(over_time_seconds))
                continue
            self.c_logger.debug(
                "Plus time!\nFrom: {} , To: {} , Minus: {} , Working hours: {}".format(
                    single_dict["from_hours_human_readable"],
                    single_dict["to_hours_human_readable"],
                    single_dict["plus_minus_human_readable"],
                    single_dict["working_hours_human_readable"],
                )
            )
            over_time = datetime.datetime.strptime("00:00", FMT) - datetime.datetime.strptime(
                single_dict["plus_minus_human_readable"].replace("+", ""), FMT
            )
            over_time_seconds -= over_time.total_seconds()
            self.c_logger.debug("Overtime is secs: {}".format(over_time_seconds))

        overtime_hours = int(divmod(abs(over_time_seconds), 3600)[0])
        overtime_mins = int(divmod(abs(over_time_seconds), 60)[0]) - (overtime_hours * 60)
        over_time_str = "{:02d}:{:02d}".format(-int(overtime_hours), int(overtime_mins))
        if over_time_seconds < 0:
            over_time_str = "-{:02d}:{:02d}".format(-int(overtime_hours), int(overtime_mins))

        self.c_logger.debug("OVERTIME: {}".format(over_time_str))

        y_ticks_plus = [abs(over_time_seconds) + x for x in range(1800, 7001, 1800)]
        y_ticks_minus = [
            abs(over_time_seconds) - x
            for x in range(1800, 7001, 1800)
            if abs(over_time_seconds) - x > 0
        ]
        y_ticks = [abs(over_time_seconds)]
        y_ticks.extend(y_ticks_plus)
        y_ticks.extend(y_ticks_minus)

        self.c_logger.debug("Y ticks: {}".format(y_ticks))

        y_tick_labels = []

        for y_tick in y_ticks:
            y_tick_hours = int(divmod(abs(y_tick), 3600)[0])
            y_tick_mins = int(divmod(abs(y_tick), 60)[0]) - (y_tick_hours * 60)
            if over_time_seconds < 0:
                y_tick_labels.append("-{:02d}:{:02d}".format(int(y_tick_hours), int(y_tick_mins)))
            else:
                y_tick_labels.append("{:02d}:{:02d}".format(int(y_tick_hours), int(y_tick_mins)))

        self.c_logger.debug("Y tick labels: {}".format(y_tick_labels))

        plus_minus__time_axis = self.axis_array[1]

        plus_minus__time_axis.set_ylim(min(y_ticks), max(y_ticks))
        plus_minus__time_axis.set_xlim(0, 0)
        self.c_logger.info("Set X label to 'Times'")
        plus_minus__time_axis.set_xlabel(self.graph_settings.get("AXIS", "overtime_x_axis_label"))
        self.c_logger.info("Set Y label to 'Dates'")

        plus_minus__time_axis.set_ylabel(self.graph_settings.get("AXIS", "overtime_y_axis_label"))

        self.c_logger.info("Set Y ticks")
        plus_minus__time_axis.set_yticks(y_ticks)
        self.c_logger.info("Y ticks: {}".format(y_ticks))

        self.c_logger.info("Set Y tick labels")
        plus_minus__time_axis.set_yticklabels(y_tick_labels)
        self.c_logger.info("Y tick labels: {}".format(y_tick_labels))

        self.c_logger.info("Set X ticks")
        plus_minus__time_axis.set_xticks([])
        self.c_logger.info("Set X tick labels")
        plus_minus__time_axis.set_xticklabels([])

        if over_time_seconds < 0:
            plus_minus__time_axis.bar(
                [0],
                abs(over_time_seconds),
                align="center",
                alpha=None,
                color=self.graph_settings.get("OVERTIME", "minus_time"),
            )
        else:
            plus_minus__time_axis.bar(
                [0],
                abs(over_time_seconds),
                align="center",
                alpha=None,
                color=self.graph_settings.get("OVERTIME", "plus_time"),
            )

    def plotting(self):
        """
        This method calls the subplots.
        Current subplots:
            - Date-Time Graph
            - Overtime Graph.
        :return: Instance of figure.
        """

        self.date_time_graph_plotting()
        if self.graph_settings.getboolean("OVERTIME", "visible"):
            self.overtime_graph_plotting()
        self.c_logger.info("Return the generated figure.")

        # Uncomment the below line if you want to test the plotting as a single file.
        # plt.show()

        return self.fig

    def date_time_graph_plotting(self):
        """
        This method plots the Date-Time Broken-Bar graph.
        :return: None
        """

        # TODO: Split this method more smaller and more understandable/readable methods.
        self.c_logger.info("Starting to plot the data")
        working_time_axis = self.axis_array[0]
        self.c_logger.info("Fig: {} , AX: {}".format(self.fig, working_time_axis))
        y_place = 2
        self.c_logger.info("Y place: {}".format(y_place))
        self.c_logger.info("Start to render the plottable data to figure.")
        for single_dict in self.plotable_dict:
            self.c_logger.debug("Single dict: {}".format(single_dict))
            self.c_logger.debug("Y place: {}".format(y_place))
            if single_dict["weekend"]:
                # IT IS A WEEKEND DAY
                self.c_logger.debug("This is a weekend day.")
                working_time_axis.broken_barh(
                    [
                        (
                            min(self.x_axis_config_data.values()),
                            max(self.x_axis_config_data.values()),
                        )
                    ],
                    (y_place, 2),
                    facecolors=self.graph_settings.get("COLORS", "weekend"),
                )

            # IF WE HAVE MINUS HOURS
            if single_dict["minus"]:
                self.c_logger.debug("There are minus hours.")
                # IF WE HAVE OFF DAY
                # TODO: Decide what should be done in case of off day. (Currently it is not visible)
                if single_dict["minus"] == 480:
                    self.c_logger.debug("This is an off day.")
                    working_time_axis.broken_barh(
                        [
                            (single_dict["from"], single_dict["to"] - single_dict["from"]),
                            (single_dict["to"], single_dict["to"],),
                        ],
                        (y_place, 2),
                        facecolors=("blue", "red"),
                        hatch="//",
                    )
                    y_place += 3
                else:
                    self.c_logger.debug("There is not an off day.")
                    working_time_axis.broken_barh(
                        [
                            (
                                single_dict["from"],
                                single_dict["to"] - single_dict["from"] - single_dict["break"],
                            ),
                            (single_dict["to"] - single_dict["break"], single_dict["break"]),
                            (single_dict["to"], single_dict["minus"] - single_dict["to"]),
                        ],
                        (y_place, 2),
                        # Working-time, Break-time, Over-Time (Minus)
                        facecolors=(
                            self.graph_settings.get("COLORS", "working_time"),
                            self.graph_settings.get("COLORS", "break_time"),
                            self.graph_settings.get("COLORS", "minus_time"),
                        ),
                        alpha=50,
                        hatch="",
                    )
                    self.create_annotate(working_time_axis, y_place, single_dict)
                    y_place += 3
            # IF WE HAVE PLUS HOURS
            else:
                self.c_logger.debug("There are plus hours")
                working_time_axis.broken_barh(
                    [
                        (
                            single_dict["from"],
                            single_dict["to"] - single_dict["from"] - single_dict["break"],
                        ),
                        (single_dict["to"] - single_dict["break"], single_dict["break"]),
                        (single_dict["to"], single_dict["plus"],),
                    ],
                    (y_place, 2),
                    # Working-time, Break-time, Over-Time (Minus)
                    facecolors=(
                        self.graph_settings.get("COLORS", "working_time"),
                        self.graph_settings.get("COLORS", "break_time"),
                        self.graph_settings.get("COLORS", "plus_time"),
                    ),
                    alpha=50,
                    hatch="",
                )
                self.create_annotate(working_time_axis, y_place, single_dict)
                y_place += 3

        self.c_logger.info("Set Y limit: 0, {}".format(self.y_axis_limit))
        working_time_axis.set_ylim(0, self.y_axis_limit)
        self.c_logger.info("Set X limit: {}, {}".format(min(self.x_axis_ticks), self.y_axis_limit))
        working_time_axis.set_xlim(min(self.x_axis_ticks), self.x_axis_limit)

        self.c_logger.info("Set X label to 'Times'")
        working_time_axis.set_xlabel(self.graph_settings.get("AXIS", "x_axis_label"))
        self.c_logger.info("Set Y label to 'Dates'")
        working_time_axis.set_ylabel(self.graph_settings.get("AXIS", "y_axis_label"))

        self.c_logger.info("Set Y ticks")
        working_time_axis.set_yticks(self.y_axis_ticks)
        self.c_logger.info("Set Y tick labels")
        working_time_axis.set_yticklabels(self.dates)

        self.c_logger.info("Set X ticks")
        working_time_axis.set_xticks(self.x_axis_ticks)
        self.c_logger.info("Set X tick labels")
        working_time_axis.set_xticklabels(self.x_axis_tick_labels, rotation=70)

        self.c_logger.info("Set grid of figure")
        working_time_axis.grid(True, linestyle=":")


####
# TEST SECTION
####


if __name__ == "__main__":
    plotter_instance = Plotter3(
        [
            {"date": "2020.03.01.", "from": "08:00", "to": "16:00"},
            {"date": "2020.03.02.", "from": "09:00", "to": "17:00"},
            {"date": "2020.03.03.", "from": "06:00", "to": "17:00"},
            {"date": "2020.03.04.", "from": "10:00", "to": "14:30"},
        ]
    )
    plotter_instance.plotting()
