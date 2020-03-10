import matplotlib.pyplot as plt
import os
import sys
import json
from datetime import datetime

# Own modules imports

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402

sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402

from helper_functions import x_axis_data_generator
from helper_functions import X_AXIS_CONFIG_FILE_PATH
from color_logger import ColoredLogger

DEFAULT_LOGGER = ColoredLogger(os.path.basename(__file__))

FMT = "%H:%M"


class Plotter3(object):
    def __init__(self, plot_data, c_logger=DEFAULT_LOGGER):

        self.c_logger = c_logger

        self.c_logger.debug("Getting plot data: {}".format(plot_data))

        self.plot_data = plot_data

        self.c_logger.info("Starting to get X axis config data.")
        self.x_axis_config_data = self.__set_x_axis_config_data()
        self.c_logger.debug("X axis config data:\n{}".format(self.x_axis_config_data))
        self.c_logger.info("X axis config data has been successfully got.")

        self.c_logger.info("Starting to calculate X axis tick labels.")
        self.x_axis_tick_labels = [
            x
            for idx, x in enumerate(self.x_axis_config_data.keys())
            if idx % 100 == 0 and idx > 240
        ]
        self.c_logger.debug("X axis tick labels:\n{}".format(self.x_axis_tick_labels))
        self.c_logger.info("X axis tick labels has been successfully calculated.")

        self.c_logger.info("Starting to calculate X axis ticks.")
        self.x_axis_ticks = [
            idx
            for idx, x in enumerate(self.x_axis_config_data.keys())
            if idx % 100 == 0 and idx > 240
        ]
        self.c_logger.debug("X axis ticks:\n{}".format(self.x_axis_ticks))
        self.c_logger.info("X axis ticks has been successfully calculated.")

        self.x_axis_limit = len(self.x_axis_config_data.keys())
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

    def __set_x_axis_config_data(self):
        self.c_logger.info("Starting to get the X axis data from config file.")
        self.c_logger.info("The used config file: {}".format(X_AXIS_CONFIG_FILE_PATH))
        if not os.path.isfile(X_AXIS_CONFIG_FILE_PATH):
            self.c_logger.warning(
                "'{}' file doesn't not exist. Call the generator method.".format(
                    X_AXIS_CONFIG_FILE_PATH
                )
            )
            x_axis_data_generator()
            self.c_logger.info("X axis data config generator method has been successfully called.")
        self.c_logger.info("Starting to open the '{}' config file.".format(X_AXIS_CONFIG_FILE_PATH))
        with open(X_AXIS_CONFIG_FILE_PATH, "r") as opened_json:
            return_x_axis_config_data = json.load(opened_json)
        self.c_logger.debug(
            "The X axis data from config file:\n{}".format(return_x_axis_config_data)
        )
        self.c_logger.info("The X axis data from the config file has been successfully parsed.")
        return return_x_axis_config_data

    def create_plottable_dict(self):
        self.c_logger.info("Starting to create the plottable dict.")
        return_times = []
        self.c_logger.info("Starting to get the elements from plotting data one by one.")
        for single_dict in self.plot_data:

            self.c_logger.debug("Single dict from plot data: {}".format(single_dict))

            time_delta = datetime.strptime(single_dict["to"], FMT) - datetime.strptime(
                single_dict["from"], FMT
            )

            self.c_logger.debug("Calculated time delta: {}".format(time_delta))

            # IF YOU HAVE PLUS TIME
            ellapsed_hours = int(divmod(time_delta.total_seconds(), 3600)[0])
            ellapsed_mins = int(divmod(time_delta.total_seconds(), 60)[0]) - (ellapsed_hours * 60)
            time_in_office = "{:02d}:{:02d}".format(int(ellapsed_hours), int(ellapsed_mins))

            effective_hours_delta = datetime.strptime(time_in_office, FMT) - datetime.strptime(
                "08:00", FMT
            )

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
                "Elapsed hours: {} , Elapsed minutes: {} , " "Plus or minus time: {}".format(
                    ellapsed_hours, ellapsed_mins, plus_or_minus_time
                )
            )

            # IF YOU HAVE MINUS TIME

            if effective_hours_delta.days < 0:
                self.c_logger.debug("You have minus time")
                effective_hours_delta = datetime.strptime("08:00", FMT) - datetime.strptime(
                    time_in_office, FMT
                )

                ellapsed_hours = int(divmod(effective_hours_delta.total_seconds(), 3600)[0])
                ellapsed_mins = int(divmod(effective_hours_delta.total_seconds(), 60)[0]) - (
                    ellapsed_hours * 60
                )

                plus_or_minus_time = "{:02d}:{:02d}".format(
                    -int(ellapsed_hours), int(ellapsed_mins)
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

            if "-" in plus_or_minus_time:
                self.c_logger.debug("'-' character is in Plus/Minus time.")
                minus_time = self.x_axis_config_data[plus_or_minus_time.replace("-", "0")]
                self.c_logger.debug("Minus time without offset: {}".format(minus_time))
                minus_time += time_offset
                self.c_logger.debug("Minus time with offset: {}".format(minus_time))
                return_times.append(
                    {
                        "from": self.x_axis_config_data[single_dict["from"]],
                        "to": self.x_axis_config_data[single_dict["to"]],
                        "minus": minus_time,
                        "plus": None,
                        "plus_minus_human_readable": plus_or_minus_time.replace("-", "-0"),
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
        self.c_logger.info("Starting to create annotates.")
        self.c_logger.debug(
            "Instance: {} , Y position: {} , Data: {}".format(instance, y_position, data)
        )
        if data["minus"]:
            instance.annotate(data["plus_minus_human_readable"], xy=(data["minus"], y_position))
            instance.annotate(
                data["to_hours_human_readable"], xy=(data["to"] - 55, y_position),
            )
        else:
            instance.annotate(
                data["plus_minus_human_readable"], xy=(data["to"] + data["plus"], y_position),
            )
            instance.annotate(
                data["to_hours_human_readable"], xy=(data["to"] + data["plus"] - 60, y_position),
            )
        instance.annotate(
            data["working_hours_human_readable"], xy=(data["from"] - 55, y_position),
        )
        instance.annotate(
            data["from_hours_human_readable"], xy=(data["from"], y_position),
        )
        self.c_logger.info("Annotates have been created successfully.")

    def plotting(self):
        self.c_logger.info("Starting to plot the data")
        fig, ax = plt.subplots(figsize=(10, 8))
        self.c_logger.info("Fig: {} , AX: {}".format(fig, ax))
        y_place = 2
        self.c_logger.info("Y place: {}".format(y_place))
        self.c_logger.info("Start to render the plottable data to figure.")
        for single_dict in self.plotable_dict:
            self.c_logger.debug("Single dict: {}".format(single_dict))
            self.c_logger.debug("Y place: {}".format(y_place))
            # IF WE HAVE MINUS HOURS
            if single_dict["minus"]:
                self.c_logger.debug("There are minus hours.")
                # IF WE HAVE OFF DAY
                if single_dict["minus"] == 480:
                    self.c_logger.debug("This is an off day.")
                    ax.broken_barh(
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
                    ax.broken_barh(
                        [
                            (single_dict["from"], single_dict["to"] - single_dict["from"]),
                            (single_dict["to"], single_dict["minus"] - single_dict["to"],),
                        ],
                        (y_place, 2),
                        facecolors=("aqua", "red"),
                        hatch="",
                    )
                    self.create_annotate(ax, y_place, single_dict)
                    y_place += 3
            # IF WE HAVE PLUS HOURS
            else:
                self.c_logger.debug("There are plus hours")
                ax.broken_barh(
                    [
                        (single_dict["from"], single_dict["to"] - single_dict["from"]),
                        (single_dict["to"], single_dict["plus"],),
                    ],
                    (y_place, 2),
                    facecolors=("aqua", "lightgreen"),
                    hatch="",
                )
                self.create_annotate(ax, y_place, single_dict)
                y_place += 3

        self.c_logger.info("Set Y limit: 0, {}".format(self.y_axis_limit))
        ax.set_ylim(0, self.y_axis_limit)
        self.c_logger.info("Set X limit: {}, {}".format(min(self.x_axis_ticks), self.y_axis_limit))
        ax.set_xlim(min(self.x_axis_ticks), self.x_axis_limit)

        self.c_logger.info("Set X label to 'Times'")
        ax.set_xlabel("Times")
        self.c_logger.info("Set Y label to 'Dates'")
        ax.set_ylabel("Dates")

        self.c_logger.info("Set Y ticks")
        ax.set_yticks(self.y_axis_ticks)
        self.c_logger.info("Set Y tick labels")
        ax.set_yticklabels(self.dates)

        self.c_logger.info("Set X ticks")
        ax.set_xticks(self.x_axis_ticks)
        self.c_logger.info("Set X tick labels")
        ax.set_xticklabels(self.x_axis_tick_labels)

        self.c_logger.info("Set grid of figure")
        ax.grid(True, linestyle=":")

        self.c_logger.info("Return the generated figure.")
        return fig
        # plt.show()


if __name__ == "__main__":
    plotter_instance = Plotter3(
        [
            {"date": "2020.03.01.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.02.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.03.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.04.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.05.", "from": "06:00", "to": "14:00"},
            {"date": "2020.03.06.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.07.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.08.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.09.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.10.", "from": "06:00", "to": "14:00"},
            {"date": "2020.03.11.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.12.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.13.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.14.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.15.", "from": "06:00", "to": "14:00"},
            {"date": "2020.03.16.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.17.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.18.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.19.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.20.", "from": "06:00", "to": "14:00"},
            {"date": "2020.03.21.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.22.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.23.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.24.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.25.", "from": "06:00", "to": "14:00"},
            {"date": "2020.03.26.", "from": "08:00", "to": "15:00"},
            {"date": "2020.03.27.", "from": "09:00", "to": "14:30"},
            {"date": "2020.03.28.", "from": "09:00", "to": "15:20"},
            {"date": "2020.03.29.", "from": "06:00", "to": "17:45"},
            {"date": "2020.03.30.", "from": "06:00", "to": "14:00"},
        ]
    )
    plotter_instance.plotting()
