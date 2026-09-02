"""
Lil' formattin' funcs
"""

from __future__ import annotations
import re, typing
import timecode

if typing.TYPE_CHECKING:
	from .trim_info import TRTTrimInfo

PAT_NATURAL_SORT_SPLIT = re.compile(r"([0-9]+)")
"""Pattern for splitting up natural sorting groups"""

PAT_PREP_TIMECODE_STRING = re.compile(r"[^0-9]+")
"""Pattern for removing non-timecode characters from a string"""

def format_string_as_timecode(timecode_string:str, timecode_rate:int=24) -> timecode.Timecode:
	"""From a given string, do our best to make it a timecode ("800" -> 8:00)"""

	# Let it be known I wrote this in one pass and it worked
	# I am a fancy timecode man

	is_negative = timecode_string.strip().startswith("-")
	stripped_input = PAT_PREP_TIMECODE_STRING.sub("", timecode_string)

	if not stripped_input:
		return timecode.Timecode("0", rate=timecode_rate)

	fps_len = len(str(timecode_rate))

	reversed_input  = stripped_input[::-1]
	reversed_parsed = []

	# Chunk the reversed string by fps length, then 2 for seconds, minutes
	for chunk_len in [fps_len, 2, 2]:

		reversed_parsed.append(reversed_input[:chunk_len])
		reversed_input = reversed_input[chunk_len:]
		if not reversed_input:
			break

	# Append remaining as hours
	if reversed_input:
		reversed_parsed.append(reversed_input)

	reversed_formatted = ":".join(reversed_parsed)

	formatted = ("-" if is_negative else "") + reversed_formatted[::-1]

	return timecode.Timecode(formatted, rate=timecode_rate)


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

def format_string_for_natural_sort(input_string:str) -> list[str,int]:
	"""Convert a string into chunked strings 'n' ints for natural sorting"""

	return [int(t) if t.isdecimal() else t.lower() for t in PAT_NATURAL_SORT_SPLIT.split(input_string)]

def format_trim_list_to_csv(trim_list:list[TRTTrimInfo]) -> str:

	from io import StringIO
	import csv

	headers = ["Name", "Runtime", "LFOA", "Trimmed From Head", "Trimmed From Tail"]

	str_buffer = StringIO()

	csv_writer = csv.DictWriter(str_buffer, headers)
	csv_writer.writeheader()

	for trim_info in trim_list:

		csv_writer.writerow({
			"Name":    trim_info.media_pool_name,
			"Runtime": format_timecode_as_duration(trim_info.runtime_range.duration),
			"LFOA":    trim_info.formatted_lfoa(),
			"Trimmed From Head": format_timecode_as_duration(trim_info.trimmed_from_head),
			"Trimmed From Tail": format_timecode_as_duration(trim_info.trimmed_from_tail),
		})

	return str_buffer.getvalue()