"""
This is the main script and it contains the all main window attributes.
Python3.6.x < Python version is required.
"""

import os
import sys
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

import main_tab as main_tab_module  # noqa: E402
from color_logger import ColoredLogger  # noqa: E402

# Set path of the window icon
PATH_OF_WINDOW_ICON = os.path.join(PATH_OF_FILE_DIR, "..", "imgs", "window_icon.png")
TEST_RUNNING = False


def main(c_logger=None):
    if not c_logger:
        # Set-up the main logger instance.
        path_of_log_file = os.path.join(PATH_OF_FILE_DIR, "..", "..", "logs", "main_log.log")
        c_logger = ColoredLogger(os.path.basename(__file__), log_file_path=path_of_log_file)
    if TEST_RUNNING:
        main_tab_module.TEST_RUNNING = True

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
    user_config_tab = tk.Frame(note)
    note.add(main_tab, text="Main")
    note.add(user_config_tab, text="User Config")
    note.pack()

    def conf(event):
        note.config(height=window.winfo_height(), width=window.winfo_width())

    start = main_tab_module.MainWindow(main_tab, c_logger=c_logger)
    window.protocol("WM_DELETE_WINDOW", start.quit_from_app)
    window.bind("<Configure>", conf)
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
