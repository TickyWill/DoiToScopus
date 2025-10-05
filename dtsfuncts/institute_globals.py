__all__ = ['INSTITUTES_LIST',
           'WORKING_FOLDERS_DICT',
          ]

# Local imports
import bmgui.gui_globals as bm_gg
import bmfuncts.institute_globals as bm_ig

# Setting institute names list
INSTITUTES_LIST = ["Liten", "Leti"]

# Setting default working folder of each institute
FILES_SUB_FOLDER = "Extractions Institut\\ScopusExtractions_Files"
FILES_FOLDER = f'BiblioMeter_Files-{bm_gg.VERSION}\\{FILES_SUB_FOLDER}'

WORKING_FOLDERS_DICT = dict(zip(INSTITUTES_LIST, [bm_ig.ROOT_FOLDERS_DICT[inst] + "\\" + FILES_FOLDER
                                                  for inst in INSTITUTES_LIST]))
