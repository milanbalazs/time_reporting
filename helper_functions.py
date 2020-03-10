import json
import os

PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402
X_AXIS_CONFIG_FILE_PATH = os.path.join(PATH_OF_FILE_DIR, "conf", "x_axis_config.json")


def x_axis_data_generator():
    counter = 0
    json_data = {}
    for hour in range(0, 21):
        for minute in range(0, 60):
            time_format = "{:02d}:{:02d}".format(hour, minute)
            json_data[time_format] = counter
            counter += 1
    with open(X_AXIS_CONFIG_FILE_PATH, "w") as opened_json:
        json.dump(json_data, opened_json)
