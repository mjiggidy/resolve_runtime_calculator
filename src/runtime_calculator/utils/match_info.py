import dataclasses, re, functools

@dataclasses.dataclass(frozen=True)
class TRTLatestMatchOptions:
	"""User options for matching "latest version" items"""

	refresh_project:bool = True
	match_string:str = ""
	match_path:str = ""
	ignore_path:str = ""

	@functools.cached_property
	def match_pattern(self) -> re.Pattern:
		"""Compiled regex match pattern"""

		escaped = re.escape(self.match_string)
		escaped = escaped.replace("\\{part\\}", r"(?P<part>\d+)", 1)
		escaped = escaped.replace("\\{version\\}", r"(?P<version>.+)", 1)

		return re.compile(escaped, re.I)