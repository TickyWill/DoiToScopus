"""The `gui_globals` module  defines the global parameters useful for the GUI settings.
"""

__all__ = ['APP_COPYRIGHT',
           'APP_LOGO',
           'APP_WIN_TITLE',
           'GUI_BUTTONS',
           'MAIN_PAGE_TITLE',
           'VERSION',
           ]

# *****************************************
# ************ GENERAL GLOBALS ************
# *****************************************

# Setting application version value
VERSION = '0.0.0'

# Setting application logo
APP_LOGO = "DTS-logo.ico"

# Setting the title of the application main window
APP_WIN_TITLE = "Extraction par DOIs de la production scientifique d'un institut"

# Copyright and contacts
APP_COPYRIGHT = ("Contributeurs et contacts :"
                 "\n- Amal Chabli : amal.chabli@orange.fr")

# *****************************************
# ********** PAGES JOINT GLOBALS **********
# *****************************************

# Initialization of the List of all the buttons
GUI_BUTTONS = []

# Setting label for each gui page
PAGES_LABELS = {'CorrectScopusPage': "Correction de l'extraction de Scopus", }

# Title of main page
MAIN_PAGE_TITLE = "- DoiToScopus -\nLancement de l'application"

