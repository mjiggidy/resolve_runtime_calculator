"""
Trim info for a given clip.  Data model element.
"""

import dataclasses
import timecode

from .formatting import format_frame_count_as_footage
from resolvecommon.itemtypes import ItemTypes

from .. import PROJECT_FRAME_RATE

FFOA_MARKER_NAME:str = "ffoa"
LFOA_MARKER_NAME:str = "lfoa"

@dataclasses.dataclass(frozen=True)
class TRTTrimOptions:
	"""Options for trim settings"""

	trim_from_head:timecode.Timecode
	trim_from_tail:timecode.Timecode

	use_ffoa_marker:bool
	use_lfoa_marker:bool

class TRTTrimInfo:
	"""Trim info (trimfo?) about a clip"""
	
	def __init__(self, media_pool_item:object, trim_options:TRTTrimOptions):
	
		self._media_pool_item = media_pool_item
		
		self._media_pool_name = self.media_pool_item.GetName()

		self._trim_options = trim_options

		self._timecode_range = timecode.TimecodeRange(
			start = timecode.Timecode(self._media_pool_item.GetClipProperty("Start TC"), rate=PROJECT_FRAME_RATE),
			duration = timecode.Timecode(self._media_pool_item.GetClipProperty("Duration"), rate=PROJECT_FRAME_RATE)
		)

		self._active_ffoa_offset = self._get_ffoa_offset()
		self._active_lfoa_offset = self._get_lfoa_offset()

		self._runtime_range = timecode.TimecodeRange(
			start = self._timecode_range.start + self._active_ffoa_offset,
			duration = max(0, (self._timecode_range.duration - self._active_ffoa_offset - self._active_lfoa_offset).frame_number)
		)

	def _get_ffoa_offset(self) -> timecode.Timecode:
		"""Calculate the actual FFOA offset to use, considering markers,  source durations, etc"""

		marker_tc = self._find_marker(FFOA_MARKER_NAME) if self._trim_options.use_ffoa_marker else None

		return min(self._timecode_range.duration, marker_tc or self._trim_options.trim_from_head)

	def _get_lfoa_offset(self):
		"""Calculate the actual LFOA offset to use, considering markers,  source durations, etc"""

		marker_tc = self._find_marker(LFOA_MARKER_NAME) if self._trim_options.use_lfoa_marker else None

		return min(self._timecode_range.duration, self._timecode_range.duration-marker_tc-1 if marker_tc is not None else self._trim_options.trim_from_tail)

	def _find_marker(self, marker_name_text:str) -> timecode.Timecode|None:
		"""Find a marker containing given text in the media pool item"""

		if ItemTypes.from_media_pool_item(self._media_pool_item) is ItemTypes.TIMELINE:
			markers = self._media_pool_item.GetTimeline().GetMarkers()
		else:
			markers = self._media_pool_item.GetMarkers()

		for frame_offset in markers:

			if marker_name_text in markers[frame_offset]["name"].casefold():
				return timecode.Timecode(int(frame_offset), rate=PROJECT_FRAME_RATE)

		return None
	
	@property
	def media_pool_item(self) -> object:
		"""A reference to the media pool item"""
		
		return self._media_pool_item
	
	@property
	def media_pool_name(self) -> str:
		"""The clip name of this item"""
		
		return self._media_pool_name
	
	@property
	def timecode_range(self) -> timecode.TimecodeRange:
		"""Full timecode range of this item (not trimmed)"""
		
		return self._timecode_range
	
	@property
	def runtime_range(self) -> timecode.TimecodeRange:
		"""The trimmed runtime range (trims applied)"""
		
		return self._runtime_range

	@property
	def trimmed_from_head(self) -> timecode.Timecode:
		"""Amount trimmed from the head"""
		
		return self._runtime_range.start - self._timecode_range.start

	@property
	def trimmed_from_tail(self) -> timecode.Timecode:
		"""Amount trimmed from the tail"""
		
		return self._timecode_range.end - self._runtime_range.end
	
	def formatted_ffoa(self, frames_per_foot:int=16) -> str:
		"""FFOA formatted as feet+frames"""

		if self._runtime_range.duration.frame_number < 1:
			return ""
		
		ffoa_frame = self.trimmed_from_head
		return format_frame_count_as_footage(ffoa_frame.frame_number, frames_per_foot)
	
	def formatted_lfoa(self, frames_per_foot:int=16) -> str:
		"""LFOA formatted as feet+frames"""
		
		self._runtime_range.duration.frame_number
		if self._runtime_range.duration.frame_number < 1:
			return ""
		
		lfoa_frame = self._runtime_range.end - self._timecode_range.start - 1
		return format_frame_count_as_footage(lfoa_frame.frame_number, frames_per_foot)