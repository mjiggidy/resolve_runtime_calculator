import timecode

from . import DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM
from .formatting import format_frame_count_as_footage
from .trim_options import TRTTrimOptions
from resolvecommon.itemtypes import ItemTypes

FFOA_MARKER_NAME:str = "ffoa"
LFOA_MARKER_NAME:str = "lfoa"

class ReelInfo:
	"""Info about a reel timeline"""
	
	def __init__(self, mediapool_item:object, trim_options:TRTTrimOptions):
	
		self._mediapool_item = mediapool_item
		
		self._mediapool_name = self.mediapool_item.GetName()

		self._trim_options = trim_options

		self._timecode_range = timecode.TimecodeRange(
			start = timecode.Timecode(self._mediapool_item.GetClipProperty("Start TC")),
			duration = timecode.Timecode(self._mediapool_item.GetClipProperty("Duration"))
		)

		ffoa_offset = self._get_ffoa_offset()
		lfoa_offset = self._get_lfoa_offset()

		self._runtime_range = timecode.TimecodeRange(
			start = self._timecode_range.start + ffoa_offset,
			duration = max(0, (self._timecode_range.duration - ffoa_offset - lfoa_offset).frame_number)
		)

	def _get_ffoa_offset(self):

		if not self._trim_options.use_ffoa_marker:
			return self._trim_options.trim_from_head

		markers = self._mediapool_item.GetTimeline().GetMarkers()

		for frame_offset in markers:

			if FFOA_MARKER_NAME in markers[frame_offset]["name"].lower():
				return timecode.Timecode(int(frame_offset))

		return self._trim_options.trim_from_head

	def _get_lfoa_offset(self):

		if not self._trim_options.use_lfoa_marker:
			return self._trim_options.trim_from_tail

		if ItemTypes.from_media_pool_item(self._mediapool_item) is ItemTypes.TIMELINE:
			markers = self._mediapool_item.GetTimeline().GetMarkers()
		else:
			markers = self._mediapool_item.GetMarkers()

		for frame_offset in markers:

			if LFOA_MARKER_NAME in markers[frame_offset]["name"].lower():
				return self._timecode_range.duration - int(frame_offset) - 1

		return self._trim_options.trim_from_tail
	
	@property
	def mediapool_item(self) -> object:
		
		return self._mediapool_item
	
	@property
	def mediapool_name(self) -> str:
		
		return self._mediapool_name
	
	@property
	def timecode_range(self) -> timecode.TimecodeRange:
		
		return self._timecode_range
	
	@property
	def runtime_range(self) -> timecode.TimecodeRange:
		
		return self._runtime_range

	@property
	def trimmed_from_head(self) -> timecode.Timecode:
		
		return self._trim_options.trim_from_head

	@property
	def trimmed_from_tail(self) -> timecode.Timecode:
		
		return self._trim_options.trim_from_tail
	
	def ffoa(self, frames_per_foot:int=16) -> str:
		
		ffoa_frames = max(self._trim_options.trim_from_head.frame_number, 0)
		return format_frame_count_as_footage(ffoa_frames, frames_per_foot)
	
	def lfoa(self, frames_per_foot:int=16) -> str:
		
		lfoa_frames = max((self._timecode_range.duration - self._trim_options.trim_from_tail).frame_number - 1, 0)
		return format_frame_count_as_footage(lfoa_frames, frames_per_foot)