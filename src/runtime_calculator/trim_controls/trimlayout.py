from ..gui.abstract_widget import TRTAbstractWidget
from ..timecode_input import tcinputcontroller

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

		self._txt_trim_head = tcinputcontroller.TRTTimecodeInputController(ui_manager=ui_manager)
		self._txt_trim_head.layout_manager().set_weight(100)
		self._txt_trim_head.layout_manager().set_minimum_size([45, 20])

		self._chk_use_ffoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use FFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_head = self._ui.HGroup([
			self._lbl_trim_head,
			self._txt_trim_head.layout(),
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_ffoa_marker,
		])

		self._lbl_trim_tail = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each tail:"
		})

		self._txt_trim_tail = tcinputcontroller.TRTTimecodeInputController(ui_manager=ui_manager)
		self._txt_trim_tail.layout_manager().set_weight(100)
		self._txt_trim_tail.layout_manager().set_minimum_size([45, 20])

		self._chk_use_lfoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use LFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_tail = self._ui.HGroup([
			self._lbl_trim_tail,
			self._txt_trim_tail.layout(),
			self._ui.HGap({"Weight":0,"MaximumSize":[20,20]}),
			self._chk_use_lfoa_marker,
		])

	def layout(self) -> object:

		return self._ui.VGroup([
			self._ctl_trim_head,
			self._ctl_trim_tail
		])

