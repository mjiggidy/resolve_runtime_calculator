__version__ = "0.1-dev"
"""Runtime Calculator version"""
# I'm gonna forget to change this I just know it

from resolvecommon.session import fusion, bmd

ui         = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

del fusion
del bmd

import timecode

DEFAULT_HEAD_TRIM = timecode.Timecode("8:00")
DEFAULT_TAIL_TRIM = timecode.Timecode("4:00")

del timecode