"""
This file contains the all Json report generator related attributes.
"""

import os
import sys
import json

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402
# Append the required directories to PATH
sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402
sys.path.append(os.path.join(PATH_OF_FILE_DIR, ".."))  # noqa: E402

from color_logger import ColoredLogger
from data_processor import DataProcessor

# TODO: Insert User info to generated file (as header) Eg.: Name, ID, SAP number etc...


class JsonReportGenerator(object):
    """
    This class contains the all Json report generator related attributes.
    """

    def __init__(self, start_date, stop_date, file_path, c_logger=None, data_processor=None):
        """
        Init method of 'JsonReportGenerator' class.
        :param start_date: The start date.
        :param stop_date: The end data.
        :param file_path: Path of the generated file.
        """

        self.start_date = start_date.replace(" ", "")
        self.stop_date = stop_date.replace(" ", "")
        self.file_path = file_path
        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.data_processor = (
            data_processor if data_processor else DataProcessor(c_logger=self.c_logger)
        )

    def logging_getting_params(self):
        """
        This method logs the getting parameters.
        :return: None
        """

        self.c_logger.debug("Start date: {}".format(self.start_date))
        self.c_logger.debug("Stop date: {}".format(self.stop_date))
        self.c_logger.debug("Generated file path: {}".format(self.file_path))

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        :return: Instance of ColoredLogger
        """

        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "json_generator.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in json_generator module.")

        return return_logger

    def get_data_structure(self):
        """
        This method provides the data from config file.
        :return: Data structure.
                 Sutructure of return format:
                    [{"date": 2020.01.01, "arriving": 9:00, "leaving": 18:00}, ...]
        """

        self.c_logger.info("Starting to get data from config to generate Json report file.")

        data_structure = []

        date_range = self.data_processor.get_time_range(self.start_date, self.stop_date)
        for single_date in date_range:
            (
                arriving,
                leaving,
                break_time,
            ) = self.data_processor.get_arriving_leaving_break_times_based_on_date(single_date)
            data_structure.append(
                {"date": single_date, "arriving": arriving, "leaving": leaving, "break": break_time}
            )

        self.c_logger.info("The Json data structure has been created successfully.")

        return data_structure

    def write_data(self):
        """
        This method writes the data to file.
        The generated file will look like:
            [
                {
                    "date": "2020.03.07.",
                    "arriving": "09:30",
                    "leaving": "17:10"
                },
                {
                    "date": "2020.03.08.",
                    "arriving": "00:00",
                    "leaving": "00:00"
                },
                {
                    "date": "2020.03.09.",
                    "arriving": "00:00",
                    "leaving": "00:00"
                }
            ]
        :return: None
        """

        self.c_logger.info("Starting to write the data to Json report file.")

        data_structure = self.get_data_structure()
        with open(self.file_path, "w") as opened_file:
            json.dump(data_structure, opened_file, indent=4)

        self.c_logger.info("Writing the data to Json report file was successful.")
