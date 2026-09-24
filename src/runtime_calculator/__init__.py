__version__ = "0.9-dev"
"""Runtime Calculator version"""
# I'm gonna forget to change this I just know it

from resolvecommon.session import resolve, fusion, bmd

ui         = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

del fusion, bmd, resolve

import timecode

DEFAULT_HEAD_TRIM:str = "8:00"
DEFAULT_TAIL_TRIM:str = "4:00"
DEFAULT_MATCH_STRING:str = "{part} v{version}"

del timecode