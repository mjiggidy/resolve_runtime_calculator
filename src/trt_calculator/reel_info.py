import timecode
from resolvecommon.versioning import Version, PAT_REEL_NAME

from . import DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM

class ReelInfo:
	"""Info about a reel timeline"""
	
	def __init__(self, timeline_mediapool_item:object, trim_from_head:timecode.Timecode|None=None, trim_from_tail:timecode.Timecode|None=None):
	
		self._timeline_mediapool_item = timeline_mediapool_item

		name_match = PAT_REEL_NAME.match(self.timeline_mediapool_item.GetName())

		if not name_match:
			raise ValueError("Timeline is not named as a reel")
		
		self._reel_number  = int(name_match.group("reel_number"))
		self._reel_name    = self.timeline_mediapool_item.GetName()
		self._reel_version = Version.from_version_string(name_match.group("reel_version"))

		self._trim_head = trim_from_head or DEFAULT_HEAD_TRIM
		self._trim_tail = trim_from_tail or DEFAULT_TAIL_TRIM

		self._timecode_range = timecode.TimecodeRange(
			start = timecode.Timecode(self._timeline_mediapool_item.GetClipProperty("Start TC")),
			duration = timecode.Timecode(self._timeline_mediapool_item.GetClipProperty("Duration"))
		)

		trimmed_start = self._timecode_range.start + self._trim_head
		trimmed_tail  = self._timecode_range.end - self._trim_tail

		# NOTE: Look into zero ranges
		self._runtime_range = timecode.TimecodeRange(
			start = trimmed_start,
			end   = trimmed_tail if trimmed_tail - trimmed_start > 0 else trimmed_start
		)
	
	@property
	def timeline_mediapool_item(self) -> object:
		
		return self._timeline_mediapool_item
	
	@property
	def reel_number(self) -> int:
		
		return self._reel_number
	
	@property
	def reel_version(self) -> Version:
		
		return self._reel_version
	
	@property
	def reel_name(self) -> int:
		
		return self._reel_name
	
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
	
	@property
	def ffoa(self) -> str:
		
		ffoa_frames = max(self._trim_head.frame_number, 0)
		return self._format_ff(ffoa_frames)
	
	@property
	def lfoa(self) -> str:
		
		lfoa_frames = max((self._timecode_range.duration - self._trim_tail).frame_number - 1, 0)

		return self._format_ff(lfoa_frames)

	@staticmethod
	def _format_ff(frame_number:int, frames_per_foot:int=16) -> str:
		return str(frame_number // frames_per_foot) + "+" + str(frame_number % frames_per_foot).zfill(len(str(frames_per_foot)))