import dataclasses
import timecode

@dataclasses.dataclass(frozen=True)
class TRTTrimOptions:
	"""Options for trim settings"""

	trim_from_head:timecode.Timecode
	trim_from_tail:timecode.Timecode

	use_ffoa_marker:bool
	use_lfoa_marker:bool