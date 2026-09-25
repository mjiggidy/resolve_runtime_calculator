import dataclasses

@dataclasses.dataclass(frozen=True)
class TRTMarkerOptions:
	"""Marker matching options"""

	ffoa_marker_name:str
	lfoa_marker_name:str