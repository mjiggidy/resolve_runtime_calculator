from .abstract_widget import TRTAbstractWidget

ID_TXT_TRIM_FFOA    = "txt_ffoa"
ID_TXT_TRIM_LFOA    = "txt_lfoa"

class TRTTrimControls(TRTAbstractWidget):

	def __init__(self, ui_manager:object, head_trim:str|None=None, tail_trim:str|None=None):

		super().__init__(ui_manager)

		self._lbl_trim_head = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each head:"
		})

		self._txt_trim_head = self._ui.LineEdit({
			"Weight": 100,
			"ID": ID_TXT_TRIM_FFOA,
			"MinimumSize": [45, 20],
			"Text": head_trim if head_trim else "",
			"PlaceholderText": "0:00",
			"Events": {"EditingFinished": True},
		})

		timecode_alignment = self._txt_trim_head.GetAlignment()
		timecode_alignment["AlignLeft"] = False
		timecode_alignment["AlignRight"] = True
		self._txt_trim_head.SetAlignment(timecode_alignment)

		self._chk_use_ffoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use FFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_head = self._ui.HGroup([
			self._lbl_trim_head,
			self._txt_trim_head,
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_ffoa_marker,
		])

		self._lbl_trim_tail = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each tail:"
		})

		self._txt_trim_tail = self._ui.LineEdit({
			"Weight": 100,
			"ID": ID_TXT_TRIM_LFOA,
			"MinimumSize": [45, 20],
			"Text": tail_trim if tail_trim else "",
			"PlaceholderText": "0:00",
			"Events": {"EditingFinished": True},
		})

		self._txt_trim_tail.SetAlignment(timecode_alignment)

		self._chk_use_lfoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use LFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_tail = self._ui.HGroup([
			self._lbl_trim_tail,
			self._txt_trim_tail,
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_lfoa_marker,
		])

	def layout(self) -> object:

		return self._ui.VGroup([
			self._ctl_trim_head,
			self._ctl_trim_tail
		])

	def set_enabled(self, is_enabled:bool):

		self._chk_use_ffoa_marker.SetEnabled(is_enabled)
		self._chk_use_lfoa_marker.SetEnabled(is_enabled)

		self._txt_trim_head.SetEnabled(is_enabled)
		self._txt_trim_tail.SetEnabled(is_enabled)

	def ffoa_trim_text(self) -> str:
		"""Return the FFOA trim amount"""

		return self._txt_trim_head.Text

	def set_ffoa_trim_text(self, formatted_duration:str):
		"""Set the FFOA trim amount"""

		self._txt_trim_head.Text = formatted_duration

	def lfoa_trim_text(self) -> str:
		"""Return the LFOA trim amount"""

		return self._txt_trim_tail.Text

	def set_lfoa_trim_text(self, formatted_duration:str):
		"""Set the LFOA trim amount"""

		self._txt_trim_tail.Text = formatted_duration

	def use_ffoa_marker(self) -> bool:
		"""Return the user's FFOA preference"""

		return self._chk_use_ffoa_marker.Checked

	def set_use_ffoa_marker(self, use_marker:bool):
		"""Set use FFOA marker"""

		self._chk_use_ffoa_marker.Checked = use_marker

	def use_lfoa_marker(self) -> bool:
		"""Return the user's LFOA preference"""

		return self._chk_use_lfoa_marker.Checked

	def set_use_lfoa_marker(self, use_marker:bool):
		"""Set use LFOA marker"""

		self._chk_use_lfoa_marker.Checked = use_marker