import timecode

from resolvecommon.session import resolve

from . import tcinputlayout, tceventdispatcher

from ..utils import formatting

class TRTTimecodeInputController:

	def __init__(self, ui_manager:object):

		self._tc_input_layout  = tcinputlayout.TRTTimecodeInputLayout(ui_manager)
		self._event_dispatcher = tceventdispatcher.TRTTimecodeInputDispatcher(controller=self)

	def register_window_handle(self, win_handle:object):

		self._event_dispatcher.register_window_handle(win_handle)

	def reformat_text(self):
		"""Reformat the input text as timecode"""

		tc_text = self.text()

		project_rate = round(resolve.GetProjectManager().GetCurrentProject().GetSetting("timelineFrameRate"))

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=project_rate)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=project_rate))

		finally:
			self.set_text(tc_formatted)

	def set_text(self, text):

		self._tc_input_layout.set_text(text)

	def text(self):

		return self._tc_input_layout.text()

	def set_enabled(self, is_enabled:bool):

		self._tc_input_layout.set_enabled(is_enabled)
		
	def layout_manager(self) -> tcinputlayout.TRTTimecodeInputLayout:

		return self._tc_input_layout

	def layout(self) -> object:

		return self.layout_manager().layout()

	def format_string_as_tc(self):
		"""Format text input to timecode"""

		tc_text = self._main_window_controller.trim_controls().lfoa_trim_text().strip().lstrip("-")

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=PROJECT_FRAME_RATE)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=PROJECT_FRAME_RATE))
		finally:
			self._main_window_controller.trim_controls().set_lfoa_trim_text(tc_formatted)