"""
This module contains the all File Type picker related attributes.
"""

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

# TODO: Pass the logger to this module.


class FileTypePicker(tk.OptionMenu):
    """
    File Type picker Class.
    It is inherited from tk.OptionMenu class.
    It contains all File type picker related attributes.
    """

    def __init__(self, parent, file_types, **kwargs):
        """
        Init method of the 'FileTypePicker' class.
        :param parent: Instance of the parent TK.
        :param file_types: The possible file types in list.
        """

        self.file_types = file_types
        if not isinstance(file_types, list) or not file_types:
            error_msg = "The 'file_types' argument is not list or it doesn't have values."
            self.show_error(title="Argument error", message=error_msg)
            raise Exception(error_msg)
        self.selected_file_type = tk.StringVar(parent, str(file_types[0]))
        super().__init__(parent, self.selected_file_type, *file_types, **kwargs)

    @staticmethod
    def show_error(title="Error", message="Error message"):
        """
        Show an error message box.
        :param title: Title of the error message box.
        :param message: Message (content) of the error message box.
        :return: None
        """

        messagebox.showerror(title, message)

    def get_file_type(self):
        """
        This method provides the current selected file type.
        :return: The current selected file type as a string.
        """

        return self.selected_file_type.get()
