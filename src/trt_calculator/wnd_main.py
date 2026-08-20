import typing
from .reel_info import ReelInfo
import timecode

BTN_ID_ADD_LATEST   = "btn_add_latest"
BTN_ID_ADD_SELECTED = "btn_add_selected"
BTN_ID_CLEAR        = "btn_clear_list"

class TRTTreeResults:
	
	def __init__(self, ui_manager:object):
		
		self._ui = ui_manager

		self._tree = self._ui.Tree({
			"Weight": 20,
			"AlternatingRowColors":True,
#			"SortingEnabled":True,
			"ItemsExpandable": False,
			"ColumnCount": 3,
			"RootIsDecorated": False,
			"UniformRowHeights": True,
			"Indentation": False,
			"Events": {},
		})

		self._tree.SetHeaderLabels([
			"Reel",
			"Runtime",
			"LFOA",
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
		
		self._tree.AddTopLevelItem(item)

	def clear(self):
		
		self._tree.Clear()

class TRTAddReelControls:
	
	def __init__(self, ui_manager:object):
		
		self._ui = ui_manager

		self._btn_add_latest   = self._ui.Button({"Weight":0, "Text":"Add Latest Reels", "ID":BTN_ID_ADD_LATEST})
		self._btn_add_selected = self._ui.Button({"Weight":0, "Text":"Add Selected", "ID":BTN_ID_ADD_SELECTED})
		self._btn_clear        = self._ui.Button({"Weight":0, "Text":"Clear", "ID":BTN_ID_CLEAR})

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
	
	def __init__(self, ui_manager:object, head_trim:timecode.Timecode|None=None, tail_trim:timecode.Timecode|None=None):
		
		self._ui = ui_manager

		self._btn_box = TRTAddReelControls(self._ui)

		self._trt_tree = TRTTreeResults(self._ui)
		self._trt_tree.tree().ColumnWidth[0] = 200
		self._trt_tree.tree().ColumnWidth[1] = 75
		self._trt_tree.tree().ColumnWidth[2] = 75

		self._status_label = self._ui.Label({"Text":"No Reels", "MinimumSize":[200,20], "Weight":0, "Events":[]})

		self._reel_infos:list[ReelInfo] = []

		self._txt_trt = self._ui.LineEdit({
			"Weight"   : 0,
			"MinimumSize": [70,20],
			"PlaceholderText":"--:--:--:--",
			"ReadOnly" : True,
			"Events"   : [],
		})

		self._lbl_trt = self._ui.Label({"Weight":0, "Text":"TRT:"})
	
	def layout(self):
		
		return self._ui.VGroup([
			self._btn_box.layout(),
			self._trt_tree.layout(),
			self._ui.HGroup([
				self._status_label,
				self._ui.HGap(),
				self._lbl_trt,
				self._txt_trt,
			]),
		])
	
	def tree_results(self) -> object:
		
		return self._trt_tree

	def set_busy(self, status_message:str|None=None):

		self._btn_box.set_enabled(False)

		if status_message is not None:
			self._status_label.Text = status_message

	def set_ready(self, status_message:str|None=None):

		self._btn_box.set_enabled(True)

		if status_message is not None:
			self._status_label.Text = status_message
	
	def add_timeline_info(self, info:ReelInfo|typing.Iterable[ReelInfo]):
		
		if isinstance(info, ReelInfo):
			info = [info]

		for reel_info in info:
			
			self._reel_infos.append(reel_info)
			
			self._trt_tree.add_text_row([
				reel_info.reel_name,
				str(reel_info.runtime_range.duration).lstrip("0:;"),
				reel_info.lfoa,
		
			])
		
		self._update_stats()

	def clear_timeline_info(self):
		
		self._trt_tree.clear()
		self._reel_infos = []

		self._update_stats()

	def _set_trt(self, trt:timecode.Timecode|None):
		
		self._txt_trt.Text = str(trt).lstrip("0:;") if trt else ""

	def _update_stats(self):
		
		self._status_label.Text = f"{len(self._reel_infos)} Reel{'' if len(self._reel_infos) == 1 else 's'}"
		self._set_trt(sum(r.runtime_range.duration for r in self._reel_infos) if self._reel_infos else None)
