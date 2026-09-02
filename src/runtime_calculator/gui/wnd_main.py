"""
Main window GUI
"""

from runtime_calculator.gui.btns_treecontrols import TRTTreeControls

from .tree_results import TRTTreeResults
from .trim_controls import TRTTrimControls
from .panel_summary import TRTSummaryPanel
from .panel_about import TRTAboutPane

from ..utils.formatting import format_timecode_as_duration
from ..utils.trim_info import TRTTrimInfo

from .. import __version__

URL_GITHUB = "https://github.com/mjiggidy/resolve_runtime_calculator"
URL_DONATE = "https://ko-fi.com/lilbinboy"

ID_WINDOW_MAIN      = "com.glowingpixel.runtimecalculator.mainwindow"



class TRTMainWindow:
	"""Main window widget"""
	
	def __init__(self, ui_manager:object, head_trim:str|None=None, tail_trim:str|None=None):
		
		self._ui = ui_manager

		self._trim_controls = TRTTrimControls(self._ui, head_trim, tail_trim)

		self._btn_box = TRTTreeControls(self._ui)

		self._trt_tree = TRTTreeResults(self._ui)
		self._trt_tree.tree().ColumnWidth[0] = 150
		self._trt_tree.tree().ColumnWidth[1] = 75
		self._trt_tree.tree().ColumnWidth[2] = 75
		self._trt_tree.tree().ColumnWidth[3] = 50
		self._trt_tree.tree().ColumnWidth[4] = 50

		self._summary_display = TRTSummaryPanel(self._ui)

		self._about_display = TRTAboutPane(self._ui, __version__, URL_GITHUB, URL_DONATE)
	
	def layout(self):
		
		return self._ui.VGroup([
			self._trim_controls.layout(),

			self._ui.Label({"FrameStyle": 4}),

			self._btn_box.layout(),
			self._trt_tree.layout(),
			self._summary_display.layout(),

			self._ui.Label({"FrameStyle": 4}),

			self._about_display.layout(),
		])
	
	def tree_results(self) -> TRTTreeResults:
		"""A reference to the trim results tree"""
		
		return self._trt_tree

	def trim_controls(self) -> TRTTrimControls:

		return self._trim_controls

	def summary_display(self) -> TRTSummaryPanel:

		return self._summary_display

	def set_busy(self, status_message:str|None=None):
		"""Set window state to busy"""

		self._btn_box.set_enabled(False)

		self._trim_controls.set_enabled(False)

		if status_message is not None:
			self._summary_display.set_status_message(status_message)

	def set_ready(self, status_message:str|None=None):
		"""Set window state to ready"""

		self._btn_box.set_enabled(True)

		self._trim_controls.set_enabled(True)

		if status_message is not None:
			self._summary_display.set_status_message(status_message)
	
	def add_timeline_info(self, info:TRTTrimInfo):
		"""Add reel info to the tree"""
		
		self._trt_tree.add_text_row([
			info.media_pool_name,
			format_timecode_as_duration(info.runtime_range.duration),
			info.formatted_lfoa(),
			format_timecode_as_duration(info.trimmed_from_head),
			format_timecode_as_duration(info.trimmed_from_tail),
		])

	def clear_trim_info(self):
		"""Clear all trim info"""
		
		self._trt_tree.clear()

