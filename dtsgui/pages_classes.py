"""Module of useful classes for GUI main management."""

__all__ = ['CorrectScopusPage',
          ]


# Standard library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

# Local imports
import bmgui.gui_globals as bm_gg
import bmgui.gui_utils as bm_gu
import bmgui.pages_utils as bm_pu
from bmgui.pages_classes import PageButton
from dtsgui.correct_scopus_page import create_correct_scopus


class CorrectScopusPage(tk.Frame):
    """Sets parsing page widgets through `create_parsing_concat` function 
    imported from `bmgui.parse_corpus_page` module.

    Args:
        master (class): `bmgui.main_page.AppMain` class.
        pagebutton_frame (tk.Frame): Frame of pages buttons.
        page_frame (tk.Frame): Frame of master page.
    """

    def __init__(self, master, pagebutton_frame, page_frame):
        super().__init__(page_frame)
        self.controller = master

        # Setting page name
        page_name = self.__class__.__name__

        # Creating and setting widgets for page button
        PageButton(master, page_name, pagebutton_frame)

        # Creating and setting widgets for page frame
        create_correct_scopus(self, master, page_name)
