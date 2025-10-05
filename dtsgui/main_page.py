""" The `main_page` module sets the `AppMain` class, its attributes and related secondary classes.
"""
__all__ = ['AppMain']

# Standard library imports
import threading
import tkinter as tk
from functools import partial
from pathlib import Path

# 3rd party imports
from screeninfo import get_monitors

# Local imports
import bmgui.gui_utils as bm_gu
import bmgui.main_utils as bm_mu
import dtsfuncts.pub_globals as dts_pg
import dtsgui.gui_globals as dts_gg
import dtsgui.main_utils as dts_mu
from bmgui.pages_classes import SetAuthorCopyright
from bmgui.pages_classes import SetMasterTitle
from dtsgui.pages_classes import CorrectScopusPage


class AppMain(tk.Tk):
    """Main class of the application.

    Traces changes in institute selection to update page parameters. 
    'wf' stands for working folder.
    """
    def __init__(self):

        # Setting the link between "self" and "tk.Tk"
        tk.Tk.__init__(self)

        # Setting useful paths
        app_functs_path = Path(__file__).parent.parent / Path('dtsfuncts')
        config_path = app_functs_path / Path(dts_pg.CONFIG_FOLDER)
        icon_path = config_path / Path(dts_gg.APP_LOGO)

        # Setting class attributes and methods (mandatory)
        _ = get_monitors()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes,'-topmost', False)
        self.iconbitmap(icon_path)

        # Initializing AppMain attributes set after working folder definition
        (AppMain.scopus_rawdata_dict, AppMain.scopus_corrected_dict,
         AppMain.scopus_to_correct_dict) = ({},) * 3

        # Setting pages classes, pages list and pages labels
        AppMain.pages = (CorrectScopusPage,)
        AppMain.pages_ordered_list = [x.__name__ for x in AppMain.pages][::-1]
        AppMain.pages_labels = dts_gg.PAGES_LABELS

        # Getting useful screen sizes and scale factors depending on displays properties
        (AppMain.win_width_px, AppMain.win_height_px, AppMain.width_sf_px, AppMain.height_sf_px,
         AppMain.width_sf_mm, AppMain.height_sf_mm) = bm_gu.general_properties(self,
                                                                               dts_gg.APP_WIN_TITLE)
        AppMain.width_sf_min = min(AppMain.width_sf_mm, AppMain.width_sf_px)
        AppMain.mid_x_pos = int(AppMain.win_width_px * 0.5)
        AppMain.sf_mm_tup = (AppMain.width_sf_mm, AppMain.height_sf_mm)

        # Setting common parameters for widgets of main page
        bm_mu.set_common_params(self, AppMain)

        # Setting widget label positions in main page
        bm_mu.set_labels_pos(self, AppMain)

        # Setting widths for displayed information
        bm_mu.set_displays_widths(self, AppMain)

        # Setting and placing widgets for title and copyright
        AppMain.main_page_title = dts_gg.MAIN_PAGE_TITLE
        AppMain.app_copyright = dts_gg.APP_COPYRIGHT
        AppMain.app_version = dts_gg.VERSION
        SetMasterTitle(self)
        SetAuthorCopyright(self)

        # Setting default values for Institute selection
        default_institute = "   "
        institute_val = tk.StringVar(self)
        institute_val.set(default_institute)
        bm_mu.set_institute_widgets(self, institute_val)

        # Tracing Institute selection
        institute_val.trace('w', partial(dts_mu.update_app_page, self,
                                         institute_widget=institute_val))

        # Handling exception
        threading.excepthook = dts_mu.except_hook
