__version__ = "0.2"
"""Runtime Calculator version"""
# I'm gonna forget to change this I just know it

from resolvecommon.session import resolve, fusion, bmd

PROJECT_FRAME_RATE:int = round(resolve.GetProjectManager().GetCurrentProject().GetSetting("timelineFrameRate"))

ui         = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

del fusion, bmd, resolve

import timecode

DEFAULT_HEAD_TRIM:str = "8:00"
DEFAULT_TAIL_TRIM:str = "4:00"

del timecode