import json
import os
import sys
from datetime import datetime
from datetime import timedelta

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402

sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402

from color_logger import ColoredLogger

CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "conf", "time_data.json")
DEFAULT_LOGGER = ColoredLogger(os.path.basename(__file__))
FMT = "%H:%M"
DATE_FORMAT = "%Y.%m.%d."


class DataProcessor(object):
    def __init__(self, config: str = CONFIG_FILE, c_logger: ColoredLogger = DEFAULT_LOGGER):
        self.config = config
        self.c_logger = c_logger
        self.c_logger.info("Getting config file: {}".format(self.config))
        self.c_logger.info("Starting to check config file existence.")
        self._check_config_exist()
        self.c_logger.info("Starting to get date from config file.")
        self.data = self.get_data()

    def _check_config_exist(self):
        self.c_logger.info("Start to check if getting config file exists.")
        if not os.path.isfile(self.config):
            error_msg = "The getting '{}' config file doesn't exist.".format(self.config)
            self.c_logger.error(error_msg)
            raise Exception(error_msg)
        self.c_logger.info("The getting '{}' config exists.".format(self.config))

    def get_data(self):
        self.c_logger.info("Start to get data from config Json file.")
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

    def set_time(self, date, start, to):
        self.c_logger.info("Start to set a new record.")
        self.c_logger.info("Date: {} ; Type: {}".format(date, type(date)))
        self.c_logger.info("Arriving: {} ; Type: {}".format(start, type(start)))
        self.c_logger.info("Leaving: {} ; Type: {}".format(to, type(to)))

        item_found = False

        for single_dict in self.data:
            self.c_logger.debug("Extracted dict: {}".format(single_dict))
            for key, value in single_dict.items():
                if key == "date" and value == date:
                    single_dict["date"] = date
                    single_dict["from"] = start
                    single_dict["to"] = to
                    item_found = True
                    break
            if item_found:
                break

        if not item_found:
            self.data.append({"date": date, "from": start, "to": to})

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

    def get_arriving_leaving_times_based_on_date(self, date):
        self.c_logger.info("Starting to get arriving and leaving time based on date.")
        self.c_logger.info("Getting date: {}".format(date))
        for single_dict in self.data:
            self.c_logger.debug("Extracted dict: {}".format(single_dict))
            for key, value in single_dict.items():
                if key == "date" and value == date:
                    self.c_logger.debug(
                        "Arriving: {} , Leaving: {}".format(single_dict["from"], single_dict["to"])
                    )
                    return single_dict["from"], single_dict["to"]
        self.c_logger.warning(
            "There is not time date for the '{}' date. Return '00:00', '00:00''".format(date)
        )
        return "00:00", "00:00"


#  TEST SECTION


if __name__ == "__main__":
    test_instance = DataProcessor()
    print(test_instance.get_data())
    print(test_instance.get_dates())
    print(test_instance.get_start_times())
    print(test_instance.get_leaving_times())
    print(test_instance.get_effective_hours())