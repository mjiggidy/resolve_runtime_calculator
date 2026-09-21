import timecode

from ..mainwindow import mainlayout
from ..utils import formatting, trim_info

class TRTMainWindowController:

	def __init__(self,
		ui_manager:object,
		/,
		trim_options:trim_info.TRTTrimOptions|None=None,
		show_nag_link:bool = True
	):

		self._ui = ui_manager
		self._main_window_layout = mainlayout.TRTMainWindowLayoutManager(
			ui_manager    = ui_manager,
			show_nag_link = show_nag_link
		)

		if trim_options:
			self.set_trim_options(trim_options)

	# Trim Options

	def set_trim_options(self, trim_objects:trim_info.TRTTrimOptions):
		"""Set all options"""

		self.set_ffoa_trim_duration(trim_objects.trim_from_head)
		self.set_lfoa_trim_duration(trim_objects.trim_from_tail)
		self.set_use_ffoa_marker(trim_objects.use_ffoa_marker)
		self.set_use_lfoa_marker(trim_objects.use_lfoa_marker)

	def trim_options(self, project_rate:int) -> trim_info.TRTTrimOptions:
		"""Get the current user trim settings"""

		return trim_info.TRTTrimOptions(
			trim_from_head  = self.ffoa_trim_duration(project_rate),
			trim_from_tail  = self.lfoa_trim_duration(project_rate),
			use_ffoa_marker = self._main_window_layout.trim_controls().use_ffoa_marker(),
			use_lfoa_marker = self._main_window_layout.trim_controls().use_lfoa_marker(),
		)	

	def set_ffoa_trim_duration(self, ffoa_duration:timecode.Timecode):
		"""Set the desired FFOA trim amount"""

		self.layout_manager().trim_controls().set_ffoa_trim_text(
			formatting.format_timecode_as_duration(ffoa_duration)
		)

	def ffoa_trim_duration(self, project_rate:int) -> timecode.Timecode:
		"""Current user-set FFOA duration"""

		return timecode.Timecode(self._main_window_layout.trim_controls().ffoa_trim_text(), rate=project_rate)
 
	def set_lfoa_trim_duration(self, lfoa_duration:timecode.Timecode):
		"""Set the desired LFOA trim amount"""

		self.layout_manager().trim_controls().set_lfoa_trim_text(
			formatting.format_timecode_as_duration(lfoa_duration)
		)

	def lfoa_trim_duration(self, project_rate:int) -> timecode.Timecode:
		"""Current user-set LFOA duration"""

		return timecode.Timecode(self._main_window_layout.trim_controls().lfoa_trim_text(), rate=project_rate)

	def set_use_ffoa_marker(self, use_ffoa_marker:bool):
		"""Toggle FFOA marker usage"""

		self._main_window_layout.trim_controls().set_use_ffoa_marker(use_ffoa_marker)

	def set_use_lfoa_marker(self, use_lfoa_marker:bool):
		"""Toggle LFOA marker usage"""

		self._main_window_layout.trim_controls().set_use_lfoa_marker(use_lfoa_marker)

	# State stuff (SS)

	def set_busy(self, status_message:str|None=None):
		"""Set window state to busy"""

		self._main_window_layout.tree_controls().set_enabled(False)
		self._main_window_layout.trim_controls().set_enabled(False)
		self._main_window_layout.button_exports().Enabled = False

		if status_message is not None:
			self._main_window_layout.status_display().set_status_message(status_message)

	def set_ready(self, status_message:str|None=None):
		"""Set window state to ready"""

		self._main_window_layout.trim_controls().set_enabled(True)

		# Enable export/clear buttons if the tree is populated
		tree_is_populated = not self._main_window_layout.tree_results().is_empty()
		self._main_window_layout.tree_controls().set_enabled(True, tree_is_populated)
		self._main_window_layout.button_exports().Enabled = tree_is_populated

		if status_message is not None:
			self._main_window_layout.status_display().set_status_message(status_message)
	
	# Trimmed item list stuff

	def add_trim_item(self, info:trim_info.TRTTrimInfo):
		"""Add reel info to the tree"""
		
		self._main_window_layout.tree_results().add_text_row([
			info.media_pool_name,
			formatting.format_timecode_as_duration(info.runtime_range.duration),
			info.formatted_lfoa(),
			formatting.format_timecode_as_duration(info.trimmed_from_head),
			formatting.format_timecode_as_duration(info.trimmed_from_tail),
		])

	def trim_item_index(self, tree_item:object) -> int:

		return self._main_window_layout.tree_results().item_index(tree_item)

	def remove_trim_item_index(self, index:int):
		"""Remove the given index"""

		self._main_window_layout.tree_results().remove_index(index)

	def clear_trim_items(self):
		"""Clear all trim info"""
		
		self._main_window_layout.tree_results().clear()

	def selected_trim_item_indexes(self) -> list[int]:

		return self._main_window_layout.tree_results().selected_rows()

	# Caluclated TRT stuff
	def set_total_runtime(self, duration:timecode.Timecode|None=None):

		trt_text = formatting.format_timecode_as_duration(duration) if duration is not None else ""

		self._main_window_layout.status_display().set_total_runtime(trt_text)

	# Layout stuff

	def layout(self) -> object:
		"""Return the layout of the widget portion of this thing"""

		return self._main_window_layout.layout()

	def layout_manager(self) -> mainlayout.TRTMainWindowLayoutManager:
		"""The widget layout manager"""

		return self._main_window_layout