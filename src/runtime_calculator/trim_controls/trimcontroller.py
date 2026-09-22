from . import trimlayout

class TRTTrimSettingsController:

	def __init__(self, ui_manager:object):

		self._trim_settings_layout = trimlayout.TRTTrimControls(ui_manager=ui_manager)

	def register_window_handle(self, win_handle:object):

		self._trim_settings_layout._txt_trim_head.register_window_handle(win_handle)
		self._trim_settings_layout._txt_trim_head.register_window_handle(win_handle)

	def layout_manager(self) -> trimlayout.TRTTrimControls:

		return self._trim_settings_layout

	def layout(self) -> object:

		return self.layout_manager().layout()

	def set_enabled(self, is_enabled:bool):

		self._trim_settings_layout._chk_use_ffoa_marker.SetEnabled(is_enabled)
		self._trim_settings_layout._chk_use_lfoa_marker.SetEnabled(is_enabled)

		self._trim_settings_layout._txt_trim_head.set_enabled(is_enabled)
		self._trim_settings_layout._txt_trim_tail.set_enabled(is_enabled)

	def ffoa_trim_text(self) -> str:
		"""Return the FFOA trim amount"""

		return self._trim_settings_layout._txt_trim_head.text()

	def set_ffoa_trim_text(self, formatted_duration:str):
		"""Set the FFOA trim amount"""

		self._trim_settings_layout._txt_trim_head.set_text(formatted_duration)

	def lfoa_trim_text(self) -> str:
		"""Return the LFOA trim amount"""

		return self._trim_settings_layout._txt_trim_tail.text()

	def set_lfoa_trim_text(self, formatted_duration:str):
		"""Set the LFOA trim amount"""

		self._trim_settings_layout._txt_trim_tail.set_text(formatted_duration)

	def use_ffoa_marker(self) -> bool:
		"""Return the user's FFOA preference"""

		return self._trim_settings_layout._chk_use_ffoa_marker.Checked

	def set_use_ffoa_marker(self, use_marker:bool):
		"""Set use FFOA marker"""

		self._trim_settings_layout._chk_use_ffoa_marker.Checked = use_marker

	def use_lfoa_marker(self) -> bool:
		"""Return the user's LFOA preference"""

		return self._trim_settings_layout._chk_use_lfoa_marker.Checked

	def set_use_lfoa_marker(self, use_marker:bool):
		"""Set use LFOA marker"""

		self._trim_settings_layout._chk_use_lfoa_marker.Checked = use_marker

		