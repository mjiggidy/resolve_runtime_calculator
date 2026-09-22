"""
Main window GUI
"""


from ..gui.btns_treecontrols import TRTTreeControls
from ..gui.tree_results import TRTTreeResults
from ..trim_controls import trimcontroller
from ..gui.panel_summary import TRTSummaryPanel
from ..gui.panel_about import TRTAboutPane

from ..gui.abstract_widget import TRTAbstractWidget

from ..utils.formatting import format_timecode_as_duration

from .. import __version__

DEFAULT_WINDOW_TITLE = "Runtime Calculator"

URL_GITHUB     = "https://github.com/mjiggidy/resolve_runtime_calculator"
URL_DONATE     = "https://ko-fi.com/lilbinboy"

ID_WINDOW_MAIN = "com.glowingpixel.runtimecalculator.mainwindow"
ID_BTN_EXPORT  = "export_trt"

class TRTMainWindowLayoutManager(TRTAbstractWidget):
	"""Main window widget"""
	
	def __init__(self,
		ui_manager:object,
		head_trim:str|None = None,
		tail_trim:str|None = None,
		show_nag_link:bool = True
	):
		
		self._ui = ui_manager

		self._trim_controls = trimcontroller.TRTTrimSettingsController(self._ui)

		self._btn_box = TRTTreeControls(self._ui)

		self._trt_tree = TRTTreeResults(self._ui)
		self._trt_tree.tree().ColumnWidth[0] = 150
		self._trt_tree.tree().ColumnWidth[1] = 75
		self._trt_tree.tree().ColumnWidth[2] = 75
		self._trt_tree.tree().ColumnWidth[3] = 50
		self._trt_tree.tree().ColumnWidth[4] = 50

		self._status_display = TRTSummaryPanel(self._ui)

		self._btn_export = self._ui.Button({
			"ID": ID_BTN_EXPORT,
			"Text": "Export Results...",
			"Enabled": False,
			"Events": {"Clicked",True},
		})

		self._about_display = TRTAboutPane(self._ui, __version__, URL_GITHUB, URL_DONATE if show_nag_link else None)
	
	def layout(self):
		
		return self._ui.VGroup([
			self._trim_controls.layout(),

			self._ui.Label({"FrameStyle": 4}),

			self._btn_box.layout(),
			self._trt_tree.layout(),
			self._status_display.layout(),
			self._btn_export,

			self._ui.Label({"FrameStyle": 4}),

			self._about_display.layout(),
		])
	
	def tree_results(self) -> TRTTreeResults:
		"""A reference to the trim results tree"""
		
		return self._trt_tree

	def tree_controls(self) -> TRTTreeControls:
		"""Add/Remove/Clear Tree Items Controls"""

		return self._btn_box

	def trim_controls(self) -> trimcontroller.TRTTrimSettingsController:
		"""FFOA/LFOA trim control options"""

		return self._trim_controls

	def status_display(self) -> TRTSummaryPanel:
		"""Status and TRT display"""

		return self._status_display

	def button_exports(self) -> object:
		"""Export button"""

		return self._btn_export
