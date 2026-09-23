"""
Main window GUI
"""


from .tree_results import TRTTreeResults
from .panel_treecontrols import TRTTreeControls
from .panel_trimoptions import TRTTrimOptionsEditor
from .panel_summary import TRTSummaryPanel
from .panel_about import TRTAboutPanel

from .abstract_widget import TRTAbstractWidget

from ..utils.formatting import format_timecode_as_duration
from ..utils.trim_info import TRTTrimInfo

from .. import __version__

DEFAULT_WINDOW_TITLE = "Runtime Calculator"

URL_GITHUB     = "https://github.com/mjiggidy/resolve_runtime_calculator"
URL_DONATE     = "https://ko-fi.com/lilbinboy"

ID_WINDOW_MAIN = "com.glowingpixel.runtimecalculator.mainwindow"
ID_BTN_EXPORT  = "export_trt"

class TRTMainWindowWidget(TRTAbstractWidget):
	"""Main window widget"""
	
	def __init__(self,
		ui_manager:object,
		head_trim:str|None = None,
		tail_trim:str|None = None,
		show_nag_link:bool = True
	):
		
		self._ui = ui_manager

		self._trim_controls = TRTTrimOptionsEditor(self._ui, head_trim, tail_trim)

		self._list_controls = TRTTreeControls(self._ui)

		self._tree_trims = TRTTreeResults(self._ui)
		self._tree_trims.tree().ColumnWidth[0] = 150
		self._tree_trims.tree().ColumnWidth[1] = 75
		self._tree_trims.tree().ColumnWidth[2] = 75
		self._tree_trims.tree().ColumnWidth[3] = 50
		self._tree_trims.tree().ColumnWidth[4] = 50

		self._summary_display = TRTSummaryPanel(self._ui)

		self._btn_export = self._ui.Button({
			"ID": ID_BTN_EXPORT,
			"Text": "Export Results...",
			"Enabled": False,
			"Events": {"Clicked",True},
		})

		self._about_panel = TRTAboutPanel(
			self._ui,
			app_version = __version__,
			url_github  = URL_GITHUB,
			url_donate  = URL_DONATE if show_nag_link else None
		)
	
	def layout(self):
		
		return self._ui.VGroup([
			self._trim_controls.layout(),

			self._ui.Label({"FrameStyle": 4}),

			self._list_controls.layout(),
			self._tree_trims.layout(),
			self._summary_display.layout(),
			self._btn_export,

			self._ui.Label({"FrameStyle": 4}),

			self._about_panel.layout(),
		])
	
	def tree_results(self) -> TRTTreeResults:
		"""A reference to the trim results tree"""
		
		return self._tree_trims

	def trim_controls(self) -> TRTTrimOptionsEditor:
		"""The Trim Options editor"""

		return self._trim_controls

	def summary_display(self) -> TRTSummaryPanel:
		"""The Summary display panel"""

		return self._summary_display

	def set_busy(self, status_message:str|None=None):
		"""Set window state to busy"""

		self._list_controls.set_enabled(False)
		self._trim_controls.set_enabled(False)
		self._btn_export.Enabled = False

		if status_message is not None:
			self._summary_display.set_status_message(status_message)

	def set_ready(self, status_message:str|None=None):
		"""Set window state to ready"""

		self._trim_controls.set_enabled(True)

		# Enable export/clear buttons if the tree is populated
		tree_is_populated = not self._tree_trims.is_empty()
		self._list_controls.set_enabled(True, tree_is_populated)
		self._btn_export.Enabled = tree_is_populated

		if status_message is not None:
			self._summary_display.set_status_message(status_message)
	
	def add_timeline_info(self, info:TRTTrimInfo):
		"""Add reel info to the tree"""
		
		self._tree_trims.add_text_row([
			info.media_pool_name,
			format_timecode_as_duration(info.runtime_range.duration),
			info.formatted_lfoa(),
			format_timecode_as_duration(info.trimmed_from_head),
			format_timecode_as_duration(info.trimmed_from_tail),
		])

	def clear_trim_info(self):
		"""Clear all trim info"""
		
		self._tree_trims.clear()

