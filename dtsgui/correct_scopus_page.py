"""The `analysis_corpus_page` module allows to perform analysis of 
impact factors, keywords and coupling.
"""

__all__ = ['create_correct_scopus']

# Standard library imports
import os
import threading
import tkinter as tk
from tkinter import messagebox

# Local imports
import bmgui.gui_globals as bm_gg
import bmgui.gui_utils as bm_gu
import bmgui.pages_utils as bm_pu
import dtsgui.gui_globals as dts_gg
from dtsfuncts.main_functs import complete_scopus
from dtsfuncts.main_functs import correct_scopus
from dtsfuncts.main_functs import save_corrected_scopus
from dtsfuncts.main_functs import set_existing_scopus_corpuses


def _launch_manu_correct(master, year_select, progress_callback):
    """Launches impact-factors analysis through `if_analysis` function 
    imported from `bmfuncts.pub_analysis` module after 
    getting year of most-recent impact factors.

    Args:
        master (class): `bmgui.main_page.AppMain` class.
        year_select (str): Corpus year defined by 4 digits.
        progress_callback (function): Function for updating \
        ProgressBar tkinter widget status.  
    """
    corr_csv_path = master.scopus_corrected_dict[year_select][0]
    to_corr_xlsx_path = master.scopus_to_correct_dict[year_select][1]
    if os.path.exists(corr_csv_path) and os.path.exists(to_corr_xlsx_path):

        # Setting the data to complete the Scopus corrected data for the selected year
        paths_list = [corr_csv_path, to_corr_xlsx_path]
        progress_callback(10)

        # Completing the Scopus corrected data with the manual corrections 
        complete_scopus(paths_list, verbose=False)    
        progress_callback(100)

        info_title = "- Information -"
        info_text = ("Les données corrigées automatiquement par DOIs ont été complétées "
                     f"avec les données corrigées manuellement pour l'année {year_select}."
                     "\n\nLes données corrigées complètes ont été sauvegardées au format csv sous :"
                     f"\n\n'{corr_csv_path}'."
                     "\n\nLe traitement par BiblioMeter peut-être lancé pour cette année "
                     "après la suppression de tous les autres fichiers à la racine du dossier.")
        messagebox.showinfo(info_title, info_text)
    else:    
        progress_callback(100)

        # Displaying up the status of the OTPs step
        warning_title = "!!! ATTENTION : fichiers manquants !!!"
        warning_text = ("Les fichiers contenant les données corrigées "
                        "et les données restant à corriger "
                        f"de l'année {year_select} ne sont pas disponibles."
                        "\n1- Effectuez la correction automatique des données "
                        "des publications avec DOIs pour cette année."
                        "\n2- Relancez la correction à partir du fichier corrigé "
                        "manuellement pour cette année.")
        messagebox.showwarning(warning_title, warning_text)



def _launch_auto_correct(master, year_select, progress_callback):
    """Launches impact-factors analysis through `if_analysis` function 
    imported from `bmfuncts.pub_analysis` module after 
    getting year of most-recent impact factors.

    Args:
        master (class): `bmgui.main_page.AppMain` class.
        year_select (str): Corpus year defined by 4 digits.
        progress_callback (function): Function for updating \
        ProgressBar tkinter widget status.  
    """
    # Setting the raw data extracted from Scopus for the selected year
    init_scopus_csv_path = master.scopus_rawdata_dict[year_select]

    # Setting the full paths for saving correction results for the selected year
    corr_scopus_paths_list = master.scopus_corrected_dict[year_select]
    to_corr_scopus_paths_list = master.scopus_to_correct_dict[year_select]

    # Building the new Scopus data through extraction by DOI
    scopus_dfs_list = correct_scopus(init_scopus_csv_path, progress_callback)

    # Saving results    
    params_list = [corr_scopus_paths_list, to_corr_scopus_paths_list]
    save_corrected_scopus(params_list, scopus_dfs_list)
    progress_callback(100)

    info_title = "- Information -"
    info_text = ("La correction automatique par DOIs de l'extraction de Scopus "
                 f"a été effectuée pour l'année {year_select}."
                 "\n\nLes données corrigées ont été sauvegardées au format csv sous :"
                 f"\n\n'{corr_scopus_paths_list[0]}'."
                 "\n\net au format xlsx sous"
                 f"\n\n'{corr_scopus_paths_list[1]}'."
                 "\n\nLes données des publications sans DOIs sont disponibles "
                 "au format xlsx pour correction sous :"
                 f"\n\n'{to_corr_scopus_paths_list[1]}'."
                 "\n\nLa correction manuelle guidée de ces données peut être lancée.")
    messagebox.showinfo(info_title, info_text)


def create_correct_scopus(self, master, page_name):
    """Manages creation and use of widgets for corpus analysis through internal 
    functions  `_launch_if_analysis`, `_launch_au_analysis`, `_launch_coupling_analysis` 
    and `_launch_kw_analysis`.

    Args:
        self (instance): Instance of the calling page.
        master (class): `bmgui.main_page.AppMain` class.
        page_name (str): Name of analysis page (`AnalyzeCorpusPage` class \
        of bmgui.main_page module).
    """

    # Internal functions

    def _update_progress(value):
        self.progress_var.set(value)
        self.progress_bar.update_idletasks()
        if value>=100:
            bm_gu.enable_buttons(self.page_buttons_list)

    # ****************************** GENERAL SETTNGS
    return_tup = set_existing_scopus_corpuses(master.wf_path,
                                              corpuses_number=None)
    (master.scopus_rawdata_dict, master.scopus_corrected_dict,
     master.scopus_to_correct_dict) = return_tup

    # Creating and setting widgets for page title and exit button
    page_label = dts_gg.PAGES_LABELS[page_name]
    bm_gu.set_page_title(self, master, page_label)
    bm_gu.set_exit_button(self, master)

    # Setting short_name for page key and year key to use in globals
    self.page_key = bm_gg.KEY_CORRECT
    self.year_key = bm_gg.KEY_CORRECT_YEAR

    # Setting progress bars parameters
    bm_pu.set_progress_bar_params(self, master)

    # Setting steps widgets parameters
    bm_pu.set_steps_widgets_param(self, master)

    # *********************** YEAR SELECTION

    default_year = master.years_list[-1]
    self.variable_years = tk.StringVar(self)
    self.variable_years.set(default_year)

    # Setting widgets for year selection
    bm_pu.set_year_select_widgets(self, master)

    # *********************** STEP 0: AUTOMATIC SCOPUS CORRECTION
    def _launch_auto_correct_try(progress_callback):
        # Getting year selection
        year_select = self.variable_years.get()

        print(f"\nAutomatic correction by DOIs launched for year {year_select}...")
        _launch_auto_correct(master, year_select, progress_callback)
        self.progress_bar.place_forget()

    def _start_launch_auto_correct_try():
        bm_gu.disable_buttons(self.page_buttons_list)
        bm_gu.place_after(auto_correct_button, self.progress_bar,
                          dx=self.progress_bar_dx, dy=self.progress_bar_dy)
        self.progress_var.set(0)
        threading.Thread(target=_launch_auto_correct_try,
                         args=(_update_progress,)).start()

    # Setting widgets of button for IF analysis
    step_num = 0
    auto_correct_help_button = bm_pu.set_step_help_button(self, step_num)
    auto_correct_button = bm_pu.set_step_launch_button(self, step_num,
                                                      _start_launch_auto_correct_try,
                                                      'bellow')

    # *********************** STEP 1: USER SCOPUS CORRECTION
    def _launch_manu_correct_try(progress_callback):
        # Getting year selection
        year_select = self.variable_years.get()

        print(f"\nManual correction launched for year {year_select}...")
        _launch_manu_correct(master, year_select, progress_callback)
        self.progress_bar.place_forget()

    def _start_launch_manu_correct_try():
        bm_gu.disable_buttons(self.page_buttons_list)
        bm_gu.place_after(manu_correct_button, self.progress_bar,
                          dx=self.progress_bar_dx, dy=self.progress_bar_dy)
        self.progress_var.set(0)
        threading.Thread(target=_launch_manu_correct_try,
                         args=(_update_progress,)).start()

    # Setting widgets of button for IF analysis
    step_num = 1
    manu_correct_help_button = bm_pu.set_step_help_button(self, step_num)
    manu_correct_button = bm_pu.set_step_launch_button(self, step_num,
                                                      _start_launch_manu_correct_try,
                                                      'bellow')

    # Setting buttons list for status change
    self.page_buttons_list = [self.years_opt_but,
                              auto_correct_help_button,
                              auto_correct_button,
                              manu_correct_help_button,
                              manu_correct_button,]
