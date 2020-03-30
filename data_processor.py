import json
import os
import sys
from datetime import datetime
from datetime import timedelta

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402

sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402

from color_logger import ColoredLogger

CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "conf", "time_data.json")
FMT = "%H:%M"
DATE_FORMAT = "%Y.%m.%d."


class DataProcessor(object):
    def __init__(self, config: str = CONFIG_FILE, c_logger: ColoredLogger = None):
        self.config = config
        self.c_logger = c_logger if c_logger else self.__set_up_default_logger()
        self.c_logger.info("Getting config file: {}".format(self.config))
        self.c_logger.info("Starting to check config file existence.")
        self._check_config_exist()
        self.c_logger.info("Starting to get date from config file.")
        self.data = self.get_data()

    @staticmethod
    def __set_up_default_logger():
        """
        Set-up a default logger if it is not provided as parameter.
        :return: Instance of ColoredLogger
        """

        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "logs", "data_processor.log")
        return_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
        return_logger.info("Default logger has been set-up in data_processor module.")

        return return_logger

    def _check_config_exist(self):
        self.c_logger.info("Start to check if getting config file exists.")
        if not os.path.isfile(self.config):
            warning_msg = "The getting '{}' config file doesn't exist.".format(self.config)
            self.c_logger.warning(warning_msg)
            try:
                open(self.config, "a").close()
            except Exception as unexpected_error:
                self.c_logger.error(
                    "Cannot create empty config file on '{}' path. ERROR: {}".format(
                        self.config, unexpected_error
                    )
                )
                raise unexpected_error
        self.c_logger.info("The getting '{}' config exists.".format(self.config))

    def get_data(self):
        self.c_logger.info("Start to get data from config Json file.")
        if os.stat(self.config).st_size == 0:
            self.c_logger.warning("The data Json file is empty.")
            return [{}]
        with open(self.config, "r") as opened_file:
            json_data = json.load(opened_file)
        self.c_logger.debug(json_data)
        self.c_logger.info("The config Json file has been successfully parsed.")
        return json_data

    def get_dates(self):
        self.c_logger.info("Parse the dates from Json config.")
        return_list = []
        self.c_logger.info("Extract the data structure")
        for dicts in self.data:
            self.c_logger.debug("Extracted dict: {}".format(dicts))
            return_list.append(dicts["date"])
        self.c_logger.debug("Parsed dates: {}".format(return_list))
        self.c_logger.info("Successfully get dates from Json config.")
        return return_list

    def get_start_times(self):
        self.c_logger.info("Parse the arriving times from Json config.")
        return_list = []
        for dicts in self.data:
            self.c_logger.debug("Extracted dict: {}".format(dicts))
            return_list.append(dicts["from"])
        self.c_logger.debug("Parsed arriving times: {}".format(return_list))
        self.c_logger.info("Successfully get arriving times from Json config.")
        return return_list

    def get_leaving_times(self):
        self.c_logger.info("Parse the leaving times from Json config.")
        return_list = []
        for dicts in self.data:
            self.c_logger.debug("Extracted dict: {}".format(dicts))
            return_list.append(dicts["to"])
        self.c_logger.debug("Parsed leaving times: {}".format(return_list))
        self.c_logger.info("Successfully get leaving times from Json config.")
        return return_list

    def get_effective_hours(self):
        self.c_logger.info("Get the effective hours based on Json config.")
        return_list = []
        for dicts in self.data:
            self.c_logger.debug("Extracted dict: {}".format(dicts))
            time_delta = datetime.strptime(dicts["to"], FMT) - datetime.strptime(dicts["from"], FMT)
            ellapsed_hours = int(divmod(time_delta.total_seconds(), 3600)[0])
            ellapsed_mins = int(divmod(time_delta.total_seconds(), 60)[0]) - (ellapsed_hours * 60)
            self.c_logger.debug(
                "Time delta: {} , Elapsed hours: {} , Elapsed minutes: {}".format(
                    time_delta, ellapsed_hours, ellapsed_mins
                )
            )
            return_list.append("{:02d}:{:02d}".format(int(ellapsed_hours), int(ellapsed_mins)))
        self.c_logger.debug("Effective hours: {}".format(return_list))
        self.c_logger.info("Successfully calculated the effective hours based on the Json config.")
        return return_list

    def set_time(self, date, start, to, break_time):
        self.c_logger.info("Start to set a new record.")
        self.c_logger.info("Date: {} ; Type: {}".format(date, type(date)))
        self.c_logger.info("Arriving: {} ; Type: {}".format(start, type(start)))
        self.c_logger.info("Leaving: {} ; Type: {}".format(to, type(to)))
        self.c_logger.info("Break: {} ; Type: {}".format(break_time, type(break_time)))

        item_found = False

        for single_dict in self.data:
            self.c_logger.debug("Extracted dict: {}".format(single_dict))
            for key, value in single_dict.items():
                if key == "date" and value == date:
                    single_dict["date"] = date
                    single_dict["from"] = start
                    single_dict["to"] = to
                    single_dict["break"] = break_time
                    item_found = True
                    break
            if item_found:
                break

        if not item_found:
            self.data.append({"date": date, "from": start, "to": to, "break": break_time})

        with open(self.config, "w") as opened_file:
            json.dump(self.data, opened_file)

    def get_time_range(self, start_date, end_date):
        self.c_logger.info("Starting to get date range.")
        self.c_logger.info("Start date: {} , End date: {}".format(start_date, end_date))
        start = datetime.strptime(start_date, DATE_FORMAT)
        end = datetime.strptime(end_date, DATE_FORMAT)
        self.c_logger.debug("Start: {} , End: {}".format(start, end))
        self.c_logger.info("Starting to generate date range.")
        date_generated = [start + timedelta(days=x) for x in range(0, (end - start).days)]
        self.c_logger.debug("Date generated: {}".format(date_generated))
        return_date_range = [date.strftime(DATE_FORMAT) for date in date_generated]
        self.c_logger.debug("Date range: {}".format(return_date_range))
        return_date_range.append(end.strftime(DATE_FORMAT))
        self.c_logger.info("The date range has been calculated successfully.")
        return return_date_range

    def get_arriving_leaving_break_times_based_on_date(self, date):
        self.c_logger.info("Starting to get arriving and leaving time based on date.")
        self.c_logger.info("Getting date: {}".format(date))
        for single_dict in self.data:
            self.c_logger.debug("Extracted dict: {}".format(single_dict))
            for key, value in single_dict.items():
                if key == "date" and value == date:
                    self.c_logger.debug(
                        "Arriving: {} , Leaving: {}".format(single_dict["from"], single_dict["to"])
                    )
                    return single_dict["from"], single_dict["to"], single_dict["break"]
        self.c_logger.warning(
            "There is not time date for the '{}' date. Return '00:00', '00:00''".format(date)
        )
        return "00:00", "00:00", "00:00"

    def validate_time_range(self, arriving, leaving):
        """
        Validate the getting time range.
        Eg.:
            If the leaving time is earlier than arriving then it is a wrong time range.
        :param arriving: Arriving time as a sting in HH:MM format
        :param leaving: Leaving time as a sting in HH:MM format
        :return: True if the time range is valid else False.
        """

        self.c_logger.info("Starting to validate the getting time range.")
        self.c_logger.debug("Arriving time: {} , Leaving time: {}".format(arriving, leaving))

        arriving_time = datetime.strptime(arriving, FMT)
        arriving_time_in_sec = arriving_time.hour * 3600 + arriving_time.minute * 60
        self.c_logger.debug(
            "Arriving hours: {} , Arriving minutes: {}".format(
                arriving_time.hour, arriving_time.minute
            )
        )
        self.c_logger.debug("Arriving time in seconds: {}".format(arriving_time_in_sec))

        leaving_time = datetime.strptime(leaving, FMT)
        leaving_time_in_sec = leaving_time.hour * 3600 + leaving_time.minute * 60
        self.c_logger.debug(
            "Leaving hours: {} , Leaving minutes: {}".format(leaving_time.hour, leaving_time.minute)
        )
        self.c_logger.debug("Leaving time in seconds: {}".format(leaving_time_in_sec))

        if leaving_time_in_sec < arriving_time_in_sec:
            self.c_logger.info("The time range is NOT correct.")
            return False

        self.c_logger.info("The time range is correct.")
        return True


#  TEST SECTION


if __name__ == "__main__":
    test_instance = DataProcessor()
    print(test_instance.get_data())
    print(test_instance.get_dates())
    print(test_instance.get_start_times())
    print(test_instance.get_leaving_times())
    print(test_instance.get_effective_hours())
