"""
This is the main script.
This script starts the GUI and other operations.
"""

import os
import sys

__author__ = "milanbalazs"
__version__ = "0.1"

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))
# Append the required directories to PATH
sys.path.append(PATH_OF_FILE_DIR)
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "gui"))

import main_gui  # noqa: E402
from color_logger import ColoredLogger  # noqa: E402

# Set-up the main logger instance.
PATH_OF_LOG_FILE = os.path.join(PATH_OF_FILE_DIR, "logs", "main_log.log")
MAIN_LOGGER = ColoredLogger(os.path.basename(__file__), log_file_path=PATH_OF_LOG_FILE)

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
        main_gui.TEST_RUNNING = True

    main_gui.main(c_logger=MAIN_LOGGER)
