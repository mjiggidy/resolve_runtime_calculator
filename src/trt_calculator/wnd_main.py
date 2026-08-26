import typing
from .formatting import format_timecode_as_duration
from .reel_info import ReelInfo

URL_GITHUB = "https://github.com/mjiggidy/resolve_runtime_calculator"
URL_DONATE = "https://ko-fi.com/lilbinboy"

ID_BTN_ADD_LATEST   = "btn_add_latest"
ID_BTN_ADD_SELECTED = "btn_add_selected"
ID_BTN_CLEAR        = "btn_clear_list"

ID_TXT_TRIM_FFOA    = "txt_ffoa"
ID_TXT_TRIM_LFOA    = "txt_lfoa"

class TRTTreeResults:
	
	def __init__(self, ui_manager:object):
		
		self._ui = ui_manager

		self._tree = self._ui.Tree({
			"Weight": 200,
			"AlternatingRowColors":True,
#			"SortingEnabled":True,
			"ItemsExpandable": False,
			"ColumnCount": 5,
			"RootIsDecorated": False,
			"UniformRowHeights": True,
			"Indentation": False,
			"Events": {},
		})

		self._tree.SetHeaderLabels([
			"Reel",
			"Runtime",
			"LFOA",
			"Head",
			"Tail",
		])

	def tree(self) -> object:
		
		return self._tree

	
	def layout(self):
		
		return self._tree
	
	def add_text_row(self, text_per_column:list[str]):
		
		item = self._tree.NewItem()

		for idx, text in enumerate(text_per_column):
			item.Text[idx] = text

		item.TextAlignment[1] = 130 # QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter  AHAHAHA I'M SMART
		item.TextAlignment[2] = 130
		item.TextAlignment[3] = 130
		item.TextAlignment[4] = 130
		
		self._tree.AddTopLevelItem(item)

#		print(dir(item.GetData))

	def clear(self):
		
		self._tree.Clear()

class TRTAddReelControls:
	
	def __init__(self, ui_manager:object):
		
		self._ui = ui_manager

		self._btn_add_latest   = self._ui.Button({"Weight":0, "Text":"Add Latest Reels", "ID":ID_BTN_ADD_LATEST})
		self._btn_add_selected = self._ui.Button({"Weight":0, "Text":"Add Selected", "ID":ID_BTN_ADD_SELECTED})
		self._btn_clear        = self._ui.Button({"Weight":0, "Text":"Clear", "ID":ID_BTN_CLEAR})

	def set_enabled(self, is_enabled:bool):

		self._btn_add_latest.Enabled = is_enabled
		self._btn_add_selected.Enabled = is_enabled
		self._btn_clear.Enabled = is_enabled
	
	def layout(self) -> object:
		
		return self._ui.HGroup([
			self._btn_add_latest,
			self._btn_add_selected,
			self._ui.HGap(),
			self._btn_clear
		])

class TRTMainWindow:
	
	def __init__(self, ui_manager:object, head_trim:str|None=None, tail_trim:str|None=None):
		
		self._ui = ui_manager



		self._btn_box = TRTAddReelControls(self._ui)

		self._lbl_trim_head = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each head:"
		})

		self._txt_trim_head = self._ui.LineEdit({
			"Weight": 0,
			"ID": ID_TXT_TRIM_FFOA,
			"MinimumSize": [50, -1],
			"Text": head_trim if head_trim else "",
			"PlaceholderText": "0:00",
			"Events": {"EditingFinished": True},
		})

		self._chk_use_ffoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use FFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_head = self._ui.HGroup([
			self._lbl_trim_head,
			self._txt_trim_head,
			self._ui.HGap(),
			self._chk_use_ffoa_marker,
		])

		self._lbl_trim_tail = self._ui.Label({
			"Weight": 0,
			"MinimumSize": [130, -1],
			"Text": "Trim from each tail:"
		})

		self._txt_trim_tail = self._ui.LineEdit({
			"Weight": 0,
			"ID": ID_TXT_TRIM_LFOA,
			"MinimumSize": [50, -1],
			"Text": tail_trim if tail_trim else "",
			"PlaceholderText": "0:00",
			"Events": {"EditingFinished": True},
		})

		self._chk_use_lfoa_marker = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Or use LFOA marker",
			"Checked": True,
			"Events": {},
		})

		self._ctl_trim_tail = self._ui.HGroup([
			self._lbl_trim_tail,
			self._txt_trim_tail,
			self._ui.HGap(),
			self._chk_use_lfoa_marker,
		])

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
			"MinimumSize": [70,20],
			"PlaceholderText": "--:--:--:--",
			"ReadOnly" : True,
			"Events"   : {},
		})

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
			"Text": f"<a href=\"{URL_GITHUB}\">Github</a> | <a href=\"{URL_DONATE}\">Donate</a>",
			"OpenExternalLinks": True,
		})
		#self._lbl_about_links.SetOpenExternalLinks(True)
		
	
	def layout(self):
		
		return self._ui.VGroup([
			self._ctl_trim_head,
			self._ctl_trim_tail,
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
	
	def tree_results(self) -> object:
		
		return self._trt_tree

	def set_busy(self, status_message:str|None=None):

		self._btn_box.set_enabled(False)

		self._chk_use_ffoa_marker.SetEnabled(False)
		self._chk_use_lfoa_marker.SetEnabled(False)

		self._txt_trim_head.SetEnabled(False)
		self._txt_trim_tail.SetEnabled(False)

		if status_message is not None:
			self._status_label.Text = status_message

	def set_ready(self, status_message:str|None=None):

		self._btn_box.set_enabled(True)

		self._chk_use_ffoa_marker.SetEnabled(True)
		self._chk_use_lfoa_marker.SetEnabled(True)

		self._txt_trim_head.SetEnabled(True)
		self._txt_trim_tail.SetEnabled(True)

		if status_message is not None:
			self._status_label.Text = status_message
	
	def add_timeline_info(self, info:ReelInfo):
		"""Add reel info to the tree"""
		
		self._trt_tree.add_text_row([
			info.mediapool_name,
			format_timecode_as_duration(info.runtime_range.duration),
			info.lfoa(),
			format_timecode_as_duration(info.trimmed_from_head),
			format_timecode_as_duration(info.trimmed_from_tail),
		])
		
#		self._update_stats()

	def clear_timeline_info(self):
		
		self._trt_tree.clear()

#		self._update_stats()

	def set_total_runtime(self, trt:str|None=None):
		"""Set the TRT results, if any"""
		
		self._txt_trt.Text = trt if trt else ""

	def set_status(self, status_text:str):
		
		self._status_label.Text = f"{len(self._reel_infos)} Reel{'' if len(self._reel_infos) == 1 else 's'}"

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

	def use_lfoa_marker(self) -> bool:
		"""Return the user's LFOA preference"""

		return self._chk_use_lfoa_marker.Checked