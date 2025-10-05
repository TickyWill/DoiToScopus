"""Module of useful functions for GUI main management."""

__all__ = ['update_app_page',
          ]


# Standard library imports
import traceback
from pathlib import Path
from tkinter import messagebox

# Local imports
import bmgui.gui_globals as bm_gg
import bmgui.gui_utils as bm_gu
import bmgui.main_utils as bm_mu
import dtsgui.gui_globals as dts_gg
import dtsfuncts.institute_globals as dts_ig
from bmgui.pages_classes import SetLaunchButton


def except_hook(args):
    """Displays raised exceptions."""
    messagebox.showerror("Error", args)
    messagebox.showerror("Exception", traceback.format_exc())
    bm_gu.enable_buttons(dts_gg.GUI_BUTTONS)


def update_app_page(self, *args, institute_widget=None):
    """Gets the selected Institute and 'datatype' widgets parameters.
    Then, trace change in datatype selection to update page parameters.

    Args:
        self (instance): Instance of the calling page.
        institute_widget (tk.StringVar): For tracking value of Institute selection.
    """
    institute_select = institute_widget.get()
    set_inst_params = False
    datatype_select = ""
    inst_default_wf = dts_ig.WORKING_FOLDERS_DICT[institute_select]
    bm_mu.set_wf_widget_param(self, institute_select, inst_default_wf,
                              datatype_select, set_inst_params)

    # Managing corpus list
    corpuses_val = bm_mu.set_corpuses_widgets_param(self, inst_default_wf)

    # Setting and displaying corpuses list initial values
    corpuses_val_to_set = ""
    default_wf_path = Path(inst_default_wf)
    info_title = "- Information -"
    info_text = ("Le test de l'accès au dossier de travail défini "
                 "par défaut peut prendre un peu de temps."
                 "\n\nMerci de patienter.")
    messagebox.showinfo(info_title, info_text)
    wf_access_status = bm_mu.try_wf_access(default_wf_path)
    if wf_access_status:
        info_title = "- Information -"
        info_text = ("L'accès au dossier de travail défini "
                     "par défaut est autorisé mais vous pouvez "
                     "en choisir un autre.")
        messagebox.showinfo(info_title, info_text)
        init_corpuses_list = bm_gu.last_available_years(default_wf_path, bm_gg.CORPUSES_NUMBER)
        corpuses_val_to_set = str(init_corpuses_list)
    corpuses_val.set(corpuses_val_to_set)

    # Managing analysis launch button
    set_inst_params = False
    SetLaunchButton(self, institute_select, default_wf_path, datatype_select, set_inst_params)
