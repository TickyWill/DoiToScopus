"""Module for setting globals specific to conferences
management and analysis.
"""

__all__ = ['CONFIG_FOLDER',
           'NO_SCOPUS_FILE',
           'ROW_COLORS',
           'SCOPUS_RAWDATA_EXTENT', 
           'XL_INDEX_BASE',
           'UNKNOWN'
          ]


# 3rd party imports
import bmfuncts.pub_globals as bm_pg


CONFIG_FOLDER = 'ConfigFiles'


UNKNOWN = "unknown"


SCOPUS_RAWDATA_EXTENT = ".csv"

NO_SCOPUS_FILE = "Missing"


XL_INDEX_BASE = bm_pg.XL_INDEX_BASE


ROW_COLORS = bm_pg.ROW_COLORS
