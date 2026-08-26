"""
Lil' formattin' funcs
"""

import timecode

def format_timecode_as_duration(timecode:timecode.Timecode, pad_to_seconds:bool=True) -> str:
	"""From a given timecode, return a string formatted for duration (trimming extraneous zeroes)"""

	stripped_tc = str(timecode).lstrip("-0:;") or "0"

	if pad_to_seconds and stripped_tc.isnumeric():
		stripped_tc = "0:" + str(timecode.frames).zfill(len(str(timecode.rate)))

	if timecode.is_negative:
		stripped_tc = "-" + stripped_tc

	return stripped_tc