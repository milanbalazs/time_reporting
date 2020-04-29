"""
This is the main script and it contains the all main window attributes.
Python3.6.x < Python version is required.
"""

import os
import sys
import configparser
from tkinter import ttk

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))
# Append the required directories to PATH
sys.path.append(os.path.join(PATH_OF_FILE_DIR, ".."))
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "tabs"))

# Import tabs
import main_tab as main_tab_module  # noqa: E402
import report_tab as report_tab_module  # noqa: E402
import user_tab as user_tab_module  # noqa: E402
import metrics_tab as metrics_tab_module  # noqa: E402

# Import own modules.
from color_logger import ColoredLogger  # noqa: E402
from data_processor import DataProcessor  # noqa: E402

# Set path of the window icon
PATH_OF_WINDOW_ICON = os.path.join(PATH_OF_FILE_DIR, "..", "imgs", "window_icon.png")
TEST_RUNNING = False
# Set test data set
TEST_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "time_data_test.json")
# Set Graph config paths
TEST_GRAPH_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "graph_config_test.ini")
USER_GRAPH_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "graph_config.ini")
DEFAULT_GRAPH_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "graph_config_default.ini")
GRAPH_CONFIG_FILE = None

# Set user config paths
TEST_USER_INFO_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "user_info_test.ini")
USER_USER_INFO_CONFIG_FILE = os.path.join(PATH_OF_FILE_DIR, "..", "conf", "user_info.ini")
USER_INFO_CONFIG_FILE = None


def set_up_graph_settings_config_parser(c_logger, config_file=None):
    """
    This method creates the config parser for the graph settings.
    :param c_logger: Instance of a common logger.
    :param config_file: Path of the related config file.
    :return: configparser object.
    """

    global GRAPH_CONFIG_FILE

    c_logger.info("Starting to set-up the graph settings config parser.")

    if not config_file:
        config_file = USER_GRAPH_CONFIG_FILE

    # Set the used config file!
    GRAPH_CONFIG_FILE = config_file

    graph_settings_config = configparser.ConfigParser()
    graph_settings_config.read(config_file)

    return graph_settings_config


def set_up_user_info_config_parser(c_logger, config_file=None):
    """
    This method creates the user info parser.
    :param c_logger: Instance of a common logger.
    :param config_file: Path of the related config file.
    :return: configparser object.
    """

    global USER_INFO_CONFIG_FILE

    c_logger.info("Starting to set-up the user config settings config parser.")

    if not config_file:
        config_file = USER_USER_INFO_CONFIG_FILE

    # Set the used config file!
    USER_INFO_CONFIG_FILE = config_file

    c_logger.debug("Used user config file: {}".format(config_file))

    user_info_config = configparser.ConfigParser()
    user_info_config.read(config_file)

    return user_info_config


def remove_unused_old_user_pics():
    """
    removing the old unused user pictures.
    :return:
    """

    if user_tab_module.UNUSED_USER_PICS:
        for path_of_old_user_pic in user_tab_module.UNUSED_USER_PICS:
            correct_pic_path = os.path.join(
                PATH_OF_FILE_DIR, "..", "imgs", path_of_old_user_pic.split(os.sep)[-1]
            )
            if (
                "default_user_pic.jpg" in correct_pic_path
                or user_tab_module.CURRENT_USED_USER_PIC.split(os.sep)[-1] in correct_pic_path
            ):
                continue
            print("Removing old not used user picture: {}".format(correct_pic_path))
            os.remove(correct_pic_path)


def quit_from_app(main_window):
    """
    Quit from application.
    :return: None
    """

    try:
        remove_unused_old_user_pics()
    except Exception as pic_removing_error:
        print(
            "[ERROR] - Cannot remove the unused user pictures.\nERROR:\n{}".format(
                pic_removing_error
            )
        )

    print("Quit from Time Reporting application.")
    main_window.quit()


def main(c_logger=None):

    if not c_logger:
        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "main_log.log")
        c_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
    if TEST_RUNNING:
        data_processor_instance = DataProcessor(config=TEST_CONFIG_FILE, c_logger=c_logger)
        graph_config_parser = set_up_graph_settings_config_parser(
            c_logger=c_logger, config_file=TEST_GRAPH_CONFIG_FILE
        )
        user_info_parser = set_up_user_info_config_parser(
            c_logger=c_logger, config_file=TEST_USER_INFO_CONFIG_FILE
        )
    else:
        data_processor_instance = DataProcessor(c_logger=c_logger)
        graph_config_parser = set_up_graph_settings_config_parser(c_logger=c_logger)
        user_info_parser = set_up_user_info_config_parser(c_logger=c_logger)

    window = tk.Tk()
    window.iconphoto(False, tk.PhotoImage(file=PATH_OF_WINDOW_ICON))
    window.title("Time reporting")

    # change ttk theme to 'clam' to fix issue with downarrow button
    style = ttk.Style()

    style.theme_create(
        "MyStyle",
        parent="alt",
        settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {"configure": {"padding": [50, 2]}},
        },
    )

    style.theme_use("MyStyle")
    note = ttk.Notebook(window)

    main_tab = tk.Frame(note)
    report_config_tab = tk.Frame(note)
    user_config_tab = tk.Frame(note)
    metrics_tab = tk.Frame(note)

    note.add(main_tab, text="Main")
    note.add(report_config_tab, text="Report")
    note.add(user_config_tab, text="User Config")
    note.add(metrics_tab, text="Metrics")

    note.pack(expand=True, fill=tk.BOTH)

    main_exit_button = tk.Button(
        window,
        width=30,
        text="EXIT",
        bg="grey60",
        activebackground="red",
        font="Helvetica 12 bold",
        command=lambda: quit_from_app(window),
    )

    main_exit_button.pack(fill=tk.X)

    main_tab_module.MainWindow(
        main_tab,
        c_logger=c_logger,
        data_processor=data_processor_instance,
        graph_settings=graph_config_parser,
        graph_settings_file_path=GRAPH_CONFIG_FILE,
    )

    report_tab_module.ReportConfigTab(
        report_config_tab, c_logger=c_logger, data_processor=data_processor_instance
    )

    user_tab_module.UserConfigTab(
        user_config_tab,
        c_logger=c_logger,
        user_info_parser=user_info_parser,
        user_info_config_file_path=USER_INFO_CONFIG_FILE,
    )

    metrics_tab_module.MetricsTab(
        metrics_tab, c_logger=c_logger, data_processor=data_processor_instance,
    )

    window.protocol("WM_DELETE_WINDOW", lambda: quit_from_app(window))

    window.mainloop()


####
# ENTRY POINT
####


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--test",
        dest="test_flag",
        help="If this flag is set, the tool uses test values.",
        action="store_true",
    )

    args = parser.parse_args()

    if args.test_flag:
        TEST_RUNNING = True

    main()
