import timecode
from resolvecommon.session import resolve

from ..utils import formatting

class TRTTimecodeInputController:
	"""Make a LineEdit be a little timecode/duration input thingy"""

	def __init__(self, line_edit:object, /, as_duration:bool=False, allow_negative:bool=True, placeholder_tc:timecode.Timecode|None=None):

		self._line_edit = line_edit

		self._allow_negative = allow_negative
		self._as_duration    = as_duration

		project_rate = round(resolve.GetProjectManager().GetCurrentProject().GetSetting("timelineFrameRate"))

		placeholder_tc   = placeholder_tc or timecode.Timecode(0, rate=project_rate)
		placeholder_text = formatting.format_timecode_as_duration(placeholder_tc) if as_duration else str(placeholder_tc)

		self._line_edit.PlaceholderText = placeholder_text

	def _on_timecode_input_changed(self, event:dict):
		"""Format user input to duration timecode"""

		self.set_from_string(self._line_edit.Text.strip())

	def set_from_string(self, timecode_string:str):
		"""Set the LineEdit text from a timecode string"""

		project_rate = round(resolve.GetProjectManager().GetCurrentProject().GetSetting("timelineFrameRate"))

		try:
			tc_from_string = formatting.format_string_as_timecode(timecode_string, timecode_rate=project_rate)

		except Exception as e:
			tc_from_string = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=project_rate))

		self.set_from_timecode(tc_from_string)

	def set_from_timecode(self, timecode:timecode.Timecode):
		"""Set the LineEdit text from a `timecode.Timecode` object"""
		
		tc_formatted = formatting.format_timecode_as_duration(timecode) if self._as_duration else str(timecode)

		if not self._allow_negative:
			tc_formatted = tc_formatted.lstrip("-")

		self._line_edit.Text = tc_formatted
		
	def register_window_handle(self, window_handle:object):
		"""Register `EditingFinished` event with dispatcher window handle"""
		
		# TODO: Figure out how to set EditingFinished event on the line edit in the constructor?

		window_handle.On[self._line_edit.ID].EditingFinished = self._on_timecode_input_changed