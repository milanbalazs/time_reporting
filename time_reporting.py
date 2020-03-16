"""
This is the main script.
This script starts the GUI and other operations.
"""

import os
import sys

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)))  # noqa: E402
# Append the required directories to PATH
sys.path.append(PATH_OF_FILE_DIR)  # noqa: E402
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "gui"))  # noqa: E402

import main_gui

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

    main_gui.main()
