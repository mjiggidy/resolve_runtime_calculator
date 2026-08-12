import timecode
from resolvecommon.session import fusion, bmd

ui         = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

del fusion
del bmd

DEFAULT_HEAD_TRIM = timecode.Timecode("8:00")
DEFAULT_TAIL_TRIM = timecode.Timecode("4:00")