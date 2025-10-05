"""Module of functions for building updated publications list extracted 
from Scopus database for the Institute selected in the GUI."""

__all__ = ['correct_scopus',
           'save_corrected_scopus',
           'set_existing_scopus_corpuses',
          ]


# Standard library imports
import os
from pathlib import Path

# 3rd party imports
import pandas as pd
import ScopusApyJson as saj
import bmgui.gui_globals as bm_gg
import bmgui.gui_utils as bm_gu
from bmfuncts.useful_functs import concat_dfs

# Local imports
import dtsfuncts.pub_globals as dts_pg


def _get_rawdata_file_path(year_folder_path, rawdata_file_end, missing_file_name):
    """Returns the name of the first rawdata file ending with 'rawdata_file_end' 
    of the folder pointed by the full path 'year_folder_path'.
    """
    filenames_list = []
    for file in os.listdir(year_folder_path):
        if file.endswith(rawdata_file_end):
            filenames_list.append(file)
    if not filenames_list:
        filenames_list.append(missing_file_name)
    rawdata_file_path = year_folder_path / Path(filenames_list[0])
    return rawdata_file_path


def _set_modif_files_path(rawdata_file_path, year_folder_path):
    # Setting useful file names
    init_scopus_file_name = str(rawdata_file_path).split('\\')[-1].split('.')[0]
    corr_scopus_file_name = f'Corr_{init_scopus_file_name}'
    to_corr_scopus_file_name = f'To_corr_{init_scopus_file_name}'

    # Setting useful paths
    corr_scopus_csv_path = year_folder_path / Path(corr_scopus_file_name + ".csv")
    to_corr_scopus_csv_path = year_folder_path / Path(to_corr_scopus_file_name + ".csv")
    corr_scopus_xlsx_path = year_folder_path / Path(corr_scopus_file_name + ".xlsx")
    to_corr_scopus_xlsx_path = year_folder_path / Path(to_corr_scopus_file_name + ".xlsx")

    corr_paths_list = [corr_scopus_csv_path, corr_scopus_xlsx_path]
    to_corr_paths_list = [to_corr_scopus_csv_path, to_corr_scopus_xlsx_path]

    return corr_paths_list, to_corr_paths_list


def set_existing_scopus_corpuses(wf_path, corpuses_number=None):
    """Sets data giving the full path to the file of data extracted from the 
    Scopus database for a list of corpus years and built the full path to 
    the new files to be created.

    The full path is given for each of the available corpuses given by the 
    `last_available_years` function imported from the "bmgui.gui_utils" module.

    Args:
        wf_path (path):  Full path to working folder.
        corpuses_number (int): The number of corpuses to be checked \
        (default: CORPUSES_NUMBER global).
    Returns:
        (dict): A dict keyyed by corpus-year folders and valued by the full path 
    to the file of data extracted from the Scopus database for the year of the corpus.
    """
    # Getting the last available corpus years
    if not corpuses_number:
        corpuses_number = bm_gg.CORPUSES_NUMBER
    year_folder_list = bm_gu.last_available_years(wf_path, corpuses_number)

    # Setting the files type of raw data
    rawdata_file_end = f'scopus{dts_pg.SCOPUS_RAWDATA_EXTENT}'
    missing_file_name = f'{dts_pg.NO_SCOPUS_FILE} {rawdata_file_end}'

    # Initializing list of file paths to build
    rawdata_file_paths_list = []
    corrected_file_paths_list = []
    to_correct_file_paths_list = []

    for year in year_folder_list:

        # Setting useful paths for corpus-year 'year'
        year_folder_path = wf_path / Path(year)
        rawdata_file_path = _get_rawdata_file_path(year_folder_path, rawdata_file_end,
                                                   missing_file_name)
        rawdata_file_paths_list.append(rawdata_file_path)

        corr_paths_list, to_corr_paths_list = _set_modif_files_path(rawdata_file_path,
                                                                    year_folder_path)
        corrected_file_paths_list.append(corr_paths_list)
        to_correct_file_paths_list.append(to_corr_paths_list)

    rawdata_dict = dict(zip(year_folder_list, rawdata_file_paths_list))
    corrected_data_dict = dict(zip(year_folder_list, corrected_file_paths_list))
    to_correct_data_dict = dict(zip(year_folder_list, to_correct_file_paths_list))

    return rawdata_dict, corrected_data_dict, to_correct_data_dict


def _replace_na(init_df):
    """Replaces NAN and "NA" values."""
    init_df.fillna(0, inplace=True)
    new_df = init_df.astype(str)
    new_df = new_df.replace(to_replace={'0': dts_pg.UNKNOWN,
                                        'NA': dts_pg.UNKNOWN})
    return new_df


def _get_init_scopus_data(scopus_file_path):
    """Sets DOIs list of initial extraction from Scopus database."""
    scopus_df = pd.read_csv(scopus_file_path, sep = ",")
    scopus_cols_list = scopus_df.columns
    scopus_df = _replace_na(scopus_df)
    scopus_df = scopus_df.reset_index()
    scopus_df = scopus_df.rename(columns={'index': 'Pub_id'})
    scopus_df['API DOI'] = scopus_df['DOI']
    scopus_df['API DOI'] = scopus_df['API DOI'].apply(lambda doi: "doi/" + str(doi).lower())
    return scopus_df, scopus_cols_list


def correct_scopus(init_scopus_file_path, progress_callback=None,  verbose=False):
    """Complements the scopus extraction with information on publications 
    of which DOIs are found in HAL extraction.
    
    Args:
        init_scopus_file_path (path): Full path to the initial Scopus extraction file.
    Returns:
        (tup): (Data of DOIs for which the extraction has been successful (dataframe) \
        Data of DOIs for which the extraction has been failed (dataframe), \
        authentication status on Scopus database (bool)).
    """
    # Initialize status
    authy_status = False

    # Setting already extracted DOIs list from scopus database
    init_scopus_df, scopus_cols_list = _get_init_scopus_data(init_scopus_file_path)        
    step_nb = len(init_scopus_df)

    new_scopus_df = pd.DataFrame(columns=scopus_cols_list)
    rest_scopus_df = init_scopus_df[scopus_cols_list].copy()

    if progress_callback:
        progress_bar_state = 10
        progress_callback(progress_bar_state)
        progress_bar_loop_progression = (100 - progress_bar_state) / step_nb

    # Build the dataframe with the results of the parsing
    # of the api request response for each DOI of the 'scopus_dois_list' list
    for idx_row, row in init_scopus_df.iterrows():
        api_doi = row['API DOI']
        doi_scopus_tup = saj.build_scopus_df_from_api([api_doi], timeout=30,
                                                      verbose=verbose)

        # Setting the data of DOIs for which the extraction has been successful
        doi_scopus_df = doi_scopus_tup[0]

        # Getting the authentication status
        authy_status = doi_scopus_tup[2]
        print(f"   Number of DOIs data requested: {idx_row} / {step_nb}", end="\r")

        if authy_status:
            if not doi_scopus_df.empty:
                doi_scopus_df = _replace_na(doi_scopus_df)
                new_scopus_df = pd.concat([new_scopus_df, doi_scopus_df])
                rest_scopus_df = rest_scopus_df.drop(idx_row)
            else:
                print("\nExtraction by DOI failed")
                print("    DOI:", api_doi)
                print("    Pub index:", row['Pub_id'])
                print("    Title:", row['Title'])

            # Updating progress bar state
            if progress_callback:
                progress_bar_state += progress_bar_loop_progression
                progress_callback(progress_bar_state)
        else:
            print("\ndoi:", api_doi)
            print("Scopus authentication failed")

            # Updating progress bar state
            if progress_callback:
                progress_callback(100)
    scopus_dfs_list = [new_scopus_df, rest_scopus_df]
    return scopus_dfs_list


def save_corrected_scopus(params_list, scopus_dfs_list, verbose=False):
    # Setting parameters values from 'params_list'
    corr_scopus_paths_list, to_corr_scopus_paths_list = params_list
    corr_scopus_csv_path, corr_scopus_xlsx_path = corr_scopus_paths_list
    to_corr_scopus_csv_path , to_corr_scopus_xlsx_path = to_corr_scopus_paths_list

    # Setting data to save from 'scopus_dfs-list'
    corr_scopus_df, to_corr_scopus_df = scopus_dfs_list

    # Saving the new Scopus data as csv file in the working folder
    corr_scopus_df.to_csv(corr_scopus_csv_path,
                          header=True, index=False, sep=',')
    if verbose:
        message = ("\n\nScopus data corrected through Scopus Api "
                  f"saved using full path:\n    {corr_scopus_csv_path}")
        print(message)

    # Saving the new Scopus data as xlsx file in the working folder
    corr_scopus_df.to_excel(corr_scopus_xlsx_path, index=False)
    if verbose:
        message = ("\n\nScopus data corrected through Scopus Api "
                  f"saved using full path:\n    {corr_scopus_xlsx_path}")
        print(message)

    # Saving the residual scopus data as csv file in the working folder
    to_corr_scopus_df.to_csv(to_corr_scopus_csv_path,
                          header=True, index=False, sep=',')
    if verbose:
        message = ("\n\nScopus data with DOIs for which extraction from Scopus database failed "
                  f"saved using full path:\n    {to_corr_scopus_csv_path}")
        print(message)


    # Saving he residual scopus data as xlsx file in the working folder
    to_corr_scopus_df.to_excel(to_corr_scopus_xlsx_path, index = False)
    if verbose:
        message = (f"\n\nScopus data with DOIs for which extraction from Scopus database failed "
                    f"saved using full path:\n    {to_corr_scopus_xlsx_path}")
        print(message)


def complete_scopus(paths_list, verbose=False):
    
    csv_scopus_file_path, xlsx_scopus_file_path = paths_list
    
    init_csv_df = pd.read_csv(csv_scopus_file_path, sep=",")
    xlsx_df = pd.read_excel(xlsx_scopus_file_path)
    final_csv_df = concat_dfs([init_csv_df, xlsx_df])
    
    final_csv_df.to_csv(csv_scopus_file_path,
                        header=True, index=False, sep=',')
    if verbose:
        message = ("\n\nScopus corrected data completed with manually corrected data "
                  f"saved using full path:\n    {csv_scopus_file_path}")
        print(message)
