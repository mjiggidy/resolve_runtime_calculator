from .abstract_widget import TRTAbstractWidget

class TRTSummaryDisplay(TRTAbstractWidget):

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		self._lbl_status = self._ui.Label({
			"Weight":0,
			"Text":"No Reels",
			"MinimumSize":[200,20],
			"Events":{}
		})

		self._txt_trt = self._ui.LineEdit({
			"Weight"   : 0,
			"MinimumSize": [80,20],
			"PlaceholderText": "--:--:--:--",
			"ReadOnly" : True,
			"Events"   : {},
		})

		trt_alignment = self._txt_trt.GetAlignment()
		trt_alignment["AlignLeft"] = False
		trt_alignment["AlignCenter"] = True
		self._txt_trt.SetAlignment(trt_alignment)

		self._lbl_trt = self._ui.Label({
			"Weight":0,
			"Text":"TRT:",
		})

	def layout(self) -> object:

		return self._ui.HGroup([
				self._lbl_status,
				self._ui.HGap(),
				self._lbl_trt,
				self._txt_trt,
			])

	def set_total_runtime(self, trt:str|None=None):
		"""Set the TRT results, if any"""
		
		self._txt_trt.Text = trt if trt else ""

	def total_runtime(self) -> str:
		"""The currently-displayed total runtime set"""

		return self._txt_trt.Text

	def set_status_message(self, message:str):
		"""Set the current status message"""

		self._lbl_status.Text = message

	def status_message(self) -> str:
		"""The currently-displayed status message"""

		return self._lbl_status.Text