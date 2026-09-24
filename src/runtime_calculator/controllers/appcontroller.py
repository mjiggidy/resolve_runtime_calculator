"""
Main app controller for the main window widget
"""

import logging, re
import timecode

from .. import DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM, DEFAULT_MATCH_STRING
from ..utils import trim_info, match_info, select_reels, formatting
from ..gui import wnd_main, wnd_settings

from . import eventdispatcher, settingscontroller

class TRTMainWindowController:
	"""Main application window controller"""

	def __init__(
		self,
		main_window_widget:wnd_main.TRTMainWindowWidget,
		/,
		trim_from_head:str   = DEFAULT_HEAD_TRIM,
		trim_from_tail:str   = DEFAULT_TAIL_TRIM,
		use_ffoa_marker:bool = True,
		use_lfoa_marker:bool = True,
		project_rate:int     = 24,
		match_string:str     = DEFAULT_MATCH_STRING,
		match_path:str       = "00 REELS",
		ignore_path:str      = "00 REELS/zArchived Reels",
		**kwargs,
	):

		if kwargs:
			logging.getLogger(__name__).debug("Got extra kwargs: %s", kwargs)

		self._main_window_widget = main_window_widget
		"""Main window widget"""

		self._event_dispatcher = eventdispatcher.TRTEventDispatcher(controller=self)

		self._reel_info_list:list[trim_info.TRTTrimInfo] = []
		"""Data model list of individual clip trim info"""

		self._match_options = match_info.TRTLatestMatchOptions(
			refresh_project = True,
			match_string    = match_string,
			match_path      = match_path,
			ignore_path     = ignore_path,
		)

		# Setup main window controller
		self._main_window_widget.trim_controls().set_trim_options(trim_info.TRTTrimOptions(
			trim_from_head  = timecode.Timecode(trim_from_head, rate=project_rate),
			trim_from_tail  = timecode.Timecode(trim_from_tail, rate=project_rate),
			use_ffoa_marker = use_ffoa_marker,
			use_lfoa_marker = use_lfoa_marker,
		))

	def event_dispatcher(self) -> eventdispatcher.TRTEventDispatcher:
		"""Return the event dispatcher"""

		return self._event_dispatcher

	def register_window_handle(self, window_handle:object):

		self._event_dispatcher.register_window_handle(window_handle)

		self._main_window_widget.trim_controls().ffoa_input_controller().register_window_handle(window_handle)
		self._main_window_widget.trim_controls().lfoa_input_controller().register_window_handle(window_handle)

	def main_window_widget(self) -> wnd_main.TRTMainWindowWidget:

		return self._main_window_widget

	def show_settings_window(self):

		from .. import dispatcher, ui

		settings_widget = wnd_settings.TRTSettingsWindow(ui)
		settings_controller = settingscontroller.TRTSettingsController(settings_widget)

		settings_handle = dispatcher.AddWindow({
			"ID": wnd_settings.ID_WINDOW_SETTINGS,
			"WindowTitle": "Settings",
			"FixedSize": [400,200],
			"Events": {"Close": True},
		}, [settings_widget.layout()])

		settings_controller.register_window_handle(settings_handle)

		settings_handle.Show()

	def add_trimmed_item_info(self, trimmed_item_info:trim_info.TRTTrimInfo):

		logging.getLogger(__name__).debug("Adding info for %s", trimmed_item_info.media_pool_name)

		self._reel_info_list.append(trimmed_item_info)
		self._main_window_widget.add_timeline_info(trimmed_item_info)

		self.refresh_total_runtime()

	def remove_trimmed_item_index(self, index:int):
		"""Remove trimfo from list and tree"""

		self._main_window_widget.set_busy("Removing...")

		try:
			self._main_window_widget.tree_results().tree().TakeTopLevelItem(index)
			del self._reel_info_list[index]
		except Exception as e:
			logging.getLogger(__name__).error("Strange error removing reel: %s", e, exc_info=True)

		self.refresh_total_runtime()

		self._main_window_widget.set_ready(f"{len(self._reel_info_list)} Item{'' if len(self._reel_info_list) == 1 else 's'}")

	def refresh_total_runtime(self):
		"""Refresh TRT calculation"""

		trt = formatting.format_timecode_as_duration(
			sum(r.runtime_range.duration for r in self._reel_info_list)
		) if self._reel_info_list else None

		self._main_window_widget.summary_display().set_total_runtime(trt)

	def close_window(self):
		"""Window is closing"""

		from .. import dispatcher

		logging.getLogger(__name__).debug("Window is closing.  And hey -- thanks.")
		dispatcher.ExitLoop(0)

	def clear_all(self):

		logging.getLogger(__name__).info("Clearing reel info")

		self._main_window_widget.set_busy("Clearing...")

		self._reel_info_list.clear()

		self._main_window_widget.clear_trim_info()
		self._main_window_widget.summary_display().set_total_runtime()

		self._main_window_widget.set_ready("Cleared")

	def add_latest_reels(self):
		
		logging.getLogger(__name__).info("Latest reels requested")


		self._main_window_widget.set_busy("Refreshing project...")
		select_reels.refresh_project()

		self._main_window_widget.set_busy("Loading latest...")

		trim_options = self.main_window_widget().trim_controls().trim_options()
		status_messages = []

		latest_reels  = []
		trimmed_reels = []
		skipped_reels = []

		try:
			latest_reels = select_reels.get_latest_from_project(self._match_options)

		except Exception as e:
			
			logging.getLogger(__name__).error("Unable to find latest reels: %s", e, exc_info=True)
			status_messages.append(str(e))

		for clip in latest_reels:

			try:
				trimmed_reels.append(trim_info.TRTTrimInfo(clip, trim_options))

			except Exception as e:
				
				logging.getLogger(__name__).error("Error adding %s: %s", clip.GetName(), e, exc_info=True)
				skipped_reels.append((clip, str(e)))

		for trimmed_reel_info in sorted(trimmed_reels, key=lambda r: formatting.format_string_for_natural_sort(r.media_pool_name)):
			self.add_trimmed_item_info(trimmed_reel_info)

		status_messages.append(f"{len(self._reel_info_list)} Item{'' if len(self._reel_info_list) == 1 else 's'}")

		if skipped_reels:
			status_messages.append(f"Skipped {len(skipped_reels)}")

		self._main_window_widget.set_ready(", ".join(status_messages))

	def add_selected_reels(self):
		
		logging.getLogger(__name__).info("Selected reels requested")


		self._main_window_widget.set_busy("Loading selected...")

		trim_options = self.main_window_widget().trim_controls().trim_options()

		trimmed_reels:list[trim_info.TRTTrimInfo] = []
		skipped_reels = []

		for clip in select_reels.get_selected_media_pool_items():

			try:
				trimmed_reels.append(trim_info.TRTTrimInfo(clip, trim_options))

			except Exception as e:
				
				logging.getLogger(__name__).error("Error adding %s: %s", clip.GetName(), e, exc_info=True)
				skipped_reels.append((clip, str(e)))

		for trimmed_reel_info in sorted(trimmed_reels, key=lambda r: formatting.format_string_for_natural_sort(r.media_pool_name)):
			self.add_trimmed_item_info(trimmed_reel_info)

		status_messages = [f"{len(self._reel_info_list)} Item{'' if len(self._reel_info_list) == 1 else 's'}"]

		if skipped_reels:
			status_messages.append(f"Skipped {len(skipped_reels)}")

		self._main_window_widget.set_ready(", ".join(status_messages))

	def remove_selected_trim_items(self):
		"""Handle key release events"""

		selected_rows = self._main_window_widget.tree_results().selected_rows()

		if not selected_rows:
			
			logging.getLogger(__name__).debug("Nothing selected to remove")
			return

		logging.getLogger(__name__).debug("Requesting to remove: %s", selected_rows)

		for idx in sorted([idx for idx,_ in selected_rows], reverse=True):
			self.remove_trimmed_item_index(idx)

	def focus_trim_item_in_media_pool(self, tree_item:object):
		"""Trim item was "activated," find it in MediaPool"""

		try:
			item_index = self._main_window_widget.tree_results().item_index(tree_item)
			trim_info = self._reel_info_list[item_index]

			select_reels.focus_media_pool_item(trim_info.media_pool_item)

		except Exception as e:
			logging.getLogger(__name__).error("Error focusing media pool item: %s", e, exc_info=True)
		else:
			logging.getLogger(__name__).debug("Focused to %s in media pool", trim_info.media_pool_name)

	def export_results(self):
		"""Export results to a file or somethin'"""

		from resolvecommon.session import resolve, fusion
		import pathlib, re

		logging.getLogger(__name__).debug("Requesting file output location")

		save_project_path = str(pathlib.Path().home() / "Desktop")
		save_project_name = " Runtime List"

		try:
			save_project_name = re.sub(r"[^a-z0-9\-_ ]+", "_", resolve.GetProjectManager().GetCurrentProject().GetName(), flags=re.I).strip() + save_project_name

		except Exception as e:
			logging.getLogger(__name__).debug("Error sanitizing project name: %s", e, exc_info=True)
			save_project_name = "My Cool" + save_project_name


		chosen_path = fusion.RequestFile(
			save_project_path,
			save_project_name,
			{
				"FReqB_Saving": True,				# Saving, not opening
				"FReqS_Filter": "CSV Files|*.csv"	# File type filter
			}
		)

		if not chosen_path:

			logging.getLogger(__name__).debug("User cancelled file selection")
			return
		
		logging.getLogger(__name__).debug("Writing results to path: %s", chosen_path)

		self._main_window_widget.set_busy()

		try:
			trt = formatting.format_timecode_as_duration(sum(r.runtime_range.duration for r in self._reel_info_list)) if self._reel_info_list else "0:00"
			with open(chosen_path, "w") as handle_export:

				print(formatting.format_trim_list_to_csv(self._reel_info_list), file=handle_export)
				print("Total Runtime: " + trt, file=handle_export)

		except Exception as e:
			logging.getLogger(__name__).error("Error writing results: %s", e, exc_info=True)
			self._main_window_widget.set_ready("Error exporting!  See logs.")

		else:
			logging.getLogger(__name__).info("Succesfully wrote results to: %s", chosen_path)
			self._main_window_widget.set_ready("CSV exported successfully")