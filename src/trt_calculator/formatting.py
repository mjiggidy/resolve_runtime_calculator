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

def format_frame_count_as_footage(frame_count:int, frames_per_foot:int=16) -> str:
	""""Given a frame count, format it as a F+F footage counter"""

	if frames_per_foot < 1:
		raise ValueError(f"Frames per foot must be a positive integer (got {frames_per_foot})")

	return ("-" if frame_count < 0 else "") + str(frame_count // frames_per_foot) + "+" + str(frame_count % frames_per_foot).zfill(len(str(frames_per_foot)))