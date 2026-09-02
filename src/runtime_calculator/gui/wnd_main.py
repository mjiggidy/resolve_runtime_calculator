"""
Main window GUI
"""

from runtime_calculator.gui.tree_controls import TRTTreeControls

from .tree_results import TRTTreeResults
from .trim_controls import TRTTrimControls

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

		self._status_label = self._ui.Label({
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

		font_about = self._ui.Font({"PointSize": 10})

		self._lbl_auth_rule = self._ui.Label({"FrameStyle": 4})  # QFrame.HLine int value.  I looked it up.

		self._lbl_about_author = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": "Written by Michael Jordan"
		})
		self._lbl_about_links  = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": f"v{__version__} | <a href=\"{URL_GITHUB}\">Github</a> | <a href=\"{URL_DONATE}\">Donate</a>",
			"OpenExternalLinks": True,
		})
		#self._lbl_about_links.SetOpenExternalLinks(True)
		
	
	def layout(self):
		
		return self._ui.VGroup([
			self._trim_controls.layout(),
			self._ui.Label({"FrameStyle": 4}),
			self._btn_box.layout(),
			self._trt_tree.layout(),
			self._ui.HGroup([
				self._status_label,
				self._ui.HGap(),
				self._lbl_trt,
				self._txt_trt,
			]),
			self._lbl_auth_rule,
			self._ui.HGroup([
				self._lbl_about_author,
				self._ui.HGap(),
				self._lbl_about_links,
			]),
		])
	
	def tree_results(self) -> TRTTreeResults:
		"""A reference to the trim results tree"""
		
		return self._trt_tree

	def trim_controls(self) -> TRTTrimControls:

		return self._trim_controls

	def set_busy(self, status_message:str|None=None):
		"""Set window state to busy"""

		self._btn_box.set_enabled(False)

		self._trim_controls.set_enabled(False)

		if status_message is not None:
			self._status_label.Text = status_message

	def set_ready(self, status_message:str|None=None):
		"""Set window state to ready"""

		self._btn_box.set_enabled(True)

		self._trim_controls.set_enabled(True)

		if status_message is not None:
			self._status_label.Text = status_message
	
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

	def set_total_runtime(self, trt:str|None=None):
		"""Set the TRT results, if any"""
		
		self._txt_trt.Text = trt if trt else ""

