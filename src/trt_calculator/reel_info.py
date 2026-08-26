import timecode

from . import DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM
from .formatting import format_frame_count_as_footage

class ReelInfo:
	"""Info about a reel timeline"""
	
	def __init__(self, mediapool_item:object, trim_from_head:timecode.Timecode|None=None, trim_from_tail:timecode.Timecode|None=None):
	
		self._mediapool_item = mediapool_item
		
		self._mediapool_name = self.mediapool_item.GetName()

		self._trim_head = trim_from_head or DEFAULT_HEAD_TRIM
		self._trim_tail = trim_from_tail or DEFAULT_TAIL_TRIM

		self._timecode_range = timecode.TimecodeRange(
			start = timecode.Timecode(self._mediapool_item.GetClipProperty("Start TC")),
			duration = timecode.Timecode(self._mediapool_item.GetClipProperty("Duration"))
		)

		trimmed_start = self._timecode_range.start + self._trim_head
		trimmed_tail  = self._timecode_range.end   - self._trim_tail

		# NOTE: Look into zero ranges
		self._runtime_range = timecode.TimecodeRange(
			start = trimmed_start,
			end   = trimmed_tail if trimmed_tail - trimmed_start > 0 else trimmed_start
		)
	
	@property
	def mediapool_item(self) -> object:
		
		return self._mediapool_item
	
	@property
	def mediapool_name(self) -> int:
		
		return self._mediapool_name
	
	@property
	def timecode_range(self) -> timecode.TimecodeRange:
		
		return self._timecode_range
	
	@property
	def runtime_range(self) -> timecode.TimecodeRange:
		
		return self._runtime_range

	@property
	def trimmed_from_head(self) -> timecode.Timecode:
		
		return self._trim_head

	@property
	def trimmed_from_tail(self) -> timecode.Timecode:
		
		return self._trim_tail
	
	def ffoa(self, frames_per_foot:int=16) -> str:
		
		ffoa_frames = max(self._trim_head.frame_number, 0)
		return format_frame_count_as_footage(ffoa_frames, frames_per_foot)
	
	def lfoa(self, frames_per_foot:int=16) -> str:
		
		lfoa_frames = max((self._timecode_range.duration - self._trim_tail).frame_number - 1, 0)
		return format_frame_count_as_footage(lfoa_frames, frames_per_foot)