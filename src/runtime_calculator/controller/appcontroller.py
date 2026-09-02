"""
Main app controller for the thing
"""

import logging, timecode

from .eventhandler import TRTEventDispatcher

from .. import dispatcher, ui, DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM, PROJECT_FRAME_RATE
from ..utils import trim_info, select_reels, formatting
from ..gui import wnd_main

MAIN_WINDOW_TITLE = "Runtime Calculator"

class TRTMainApplication:
	"""Main application controller"""

	def __init__(
		self,
		trim_from_head:str   = DEFAULT_HEAD_TRIM,
		trim_from_tail:str   = DEFAULT_TAIL_TRIM,
		use_ffoa_marker:bool = True,
		use_lfoa_marker:bool = True,
		project_rate:int     = 24
	):

		self._trt_main_window = wnd_main.TRTMainWindow(ui)
		"""Main window controller"""

		win = self._setup_window()

		self._event_dispatcher = TRTEventDispatcher(controller=self, window_handle=win)

		self._reel_info_list:list[trim_info.TRTTrimInfo] = []
		"""Data model list of individual clip trim info"""

		self._current_trim_options = trim_info.TRTTrimOptions(
			trim_from_head  = timecode.Timecode(trim_from_head, rate=project_rate),
			trim_from_tail  = timecode.Timecode(trim_from_tail, rate=project_rate),
			use_ffoa_marker = use_ffoa_marker,
			use_lfoa_marker = use_lfoa_marker,
		)
		"""Currently-active trim options"""

		# Setup main window controller
		self._trt_main_window.trim_controls().set_ffoa_trim_text(formatting.format_timecode_as_duration(self._current_trim_options.trim_from_head))
		self._trt_main_window.trim_controls().set_lfoa_trim_text(formatting.format_timecode_as_duration(self._current_trim_options.trim_from_tail))
		self._trt_main_window.trim_controls().set_use_ffoa_marker(self._current_trim_options.use_ffoa_marker)
		self._trt_main_window.trim_controls().set_use_lfoa_marker(self._current_trim_options.use_lfoa_marker)

		# Add mainwindow to  UIDispatcher
		win.Show()
		dispatcher.RunLoop()

	def _setup_window(self) -> object:

		if win:= ui.FindWindow(wnd_main.ID_WINDOW_MAIN):

			win.Show()
			win.Raise()
			
			import sys
			sys.exit(0)

		# Use trim options if passsed, otherwise use the defaults
		
		win = dispatcher.AddWindow({
			"ID": wnd_main.ID_WINDOW_MAIN,
			"WindowTitle": MAIN_WINDOW_TITLE,
			"FixedSize": [360,500],
			"Events": {"Close": True, "KeyRelease": True},
		}, [self._trt_main_window.layout()])

		return win

	def current_trim_options(self) -> trim_info.TRTTrimOptions:

		return self._current_trim_options

	def update_trim_options_from_window(self) -> trim_info.TRTTrimOptions:

		self._current_trim_options = trim_info.TRTTrimOptions(
			trim_from_head = timecode.Timecode(self._trt_main_window.trim_controls().ffoa_trim_text(), rate=PROJECT_FRAME_RATE),
			trim_from_tail = timecode.Timecode(self._trt_main_window.trim_controls().lfoa_trim_text(), rate=PROJECT_FRAME_RATE),
			use_ffoa_marker = self._trt_main_window.trim_controls().use_ffoa_marker(),
			use_lfoa_marker = self._trt_main_window.trim_controls().use_lfoa_marker(),
		)

		return self._current_trim_options

	def add_trimmed_item_info(self, trimmed_item_info:trim_info.TRTTrimInfo):

		logging.getLogger(__name__).debug("Adding info for %s", trimmed_item_info.media_pool_name)

		self._reel_info_list.append(trimmed_item_info)
		self._trt_main_window.add_timeline_info(trimmed_item_info)

		self.refresh_total_runtime()

	def remove_trimmed_item_index(self, index:int):
		"""Remove trimfo from list and tree"""

		self._trt_main_window.set_busy("Removing...")

		try:
			self._trt_main_window.tree_results().tree().TakeTopLevelItem(index)
			del self._reel_info_list[index]
		except Exception as e:
			logging.getLogger(__name__).error("Strange error removing reel: %s", e, exc_info=True)

		self.refresh_total_runtime()

		self._trt_main_window.set_ready(f"{len(self._reel_info_list)} Item{'' if len(self._reel_info_list) == 1 else 's'}")

	def refresh_total_runtime(self):
		"""Refresh TRT calculation"""

		trt = formatting.format_timecode_as_duration(
			sum(r.runtime_range.duration for r in self._reel_info_list)
		) if self._reel_info_list else None

		self._trt_main_window.summary_display().set_total_runtime(trt)

	def close_window(self):
		"""Window is closing"""

		# Update options for later writing to disk
		self.update_trim_options_from_window()

		logging.getLogger(__name__).debug("Window is closing.  And hey -- thanks.")
		dispatcher.ExitLoop(0)

	def clear_all(self):

		logging.getLogger(__name__).info("Clearing reel info")

		self._trt_main_window.set_busy("Clearing...")

		self._reel_info_list.clear()

		self._trt_main_window.clear_trim_info()
		self._trt_main_window.summary_display().set_total_runtime()

		self._trt_main_window.set_ready("Cleared")

	def add_latest_reels(self):
		
		logging.getLogger(__name__).info("Latest reels requested")


		self._trt_main_window.set_busy("Refreshing project...")
		select_reels.refresh_project()

		self._trt_main_window.set_busy("Loading latest...")

		trim_options = self.update_trim_options_from_window()

		latest_reels  = []
		trimmed_reels = []
		skipped_reels = []


		try:
			latest_reels = select_reels.get_latest_reels_from_project()

		except Exception as e:
			logging.getLogger(__name__).error("Unable to find latest reels: %s", e, exc_info=True)

		for clip in latest_reels:

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

		self._trt_main_window.set_ready(", ".join(status_messages))

	def add_selected_reels(self):
		
		logging.getLogger(__name__).info("Selected reels requested")


		self._trt_main_window.set_busy("Loading selected...")

		trim_options = self.update_trim_options_from_window()

		trimmed_reels:list[trim_info.TRTTrimInfo] = []
		skipped_reels = []

		for clip in select_reels.get_selected_reels():

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

		self._trt_main_window.set_ready(", ".join(status_messages))

	def validate_ffoa_trim_amount(self):
		"""Validate FFOA trim amount"""

		tc_text = self._trt_main_window.trim_controls().ffoa_trim_text().strip().lstrip("-")

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=PROJECT_FRAME_RATE)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=PROJECT_FRAME_RATE))
		finally:
			self._trt_main_window.trim_controls().set_ffoa_trim_text(tc_formatted)

	def validate_lfoa_trim_amount(self):
		"""Validate LFOA trim amount"""

		tc_text = self._trt_main_window.trim_controls().lfoa_trim_text().strip().lstrip("-")

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=PROJECT_FRAME_RATE)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=PROJECT_FRAME_RATE))
		finally:
			self._trt_main_window.trim_controls().set_lfoa_trim_text(tc_formatted)

	def remove_selected_trim_items(self):
		"""Handle key release events"""

		selected_rows = self._trt_main_window.tree_results().selected_rows()

		if not selected_rows:
			
			logging.getLogger(__name__).debug("Nothing selected to remove")
			return

		logging.getLogger(__name__).debug("Requesting to remove: %s", selected_rows)

		for idx in sorted([idx for idx,_ in selected_rows], reverse=True):
			self.remove_trimmed_item_index(idx)

	def focus_trim_item_in_media_pool(self, tree_item:object):
		"""Trim item was "activated," find it in MediaPool"""

		try:
			item_index = self._trt_main_window.tree_results().item_index(tree_item)
			trim_info = self._reel_info_list[item_index]

			select_reels.focus_reel(trim_info.media_pool_item)

		except Exception as e:
			logging.getLogger(__name__).error("Error focusing media pool item: %s", e, exc_info=True)
		else:
			logging.getLogger(__name__).debug("Focused to %s in media pool", trim_info.media_pool_name)

	def export_results(self):
		"""Export results to a file or somethin'"""

		from resolvecommon.session import resolve, fusion

		result = fusion.RequestFile(
			"/Users/editor/Desktop/",
			resolve.GetCurrentProject().GetName() + "_Runtime.csv",
			{
				"FReqB_Saving": True,
				"FReqS_Filter": "CSV Files|*.csv"
			}
		)

		if not result:

			logging.getLogger(__name__).debug("User cancelled file selection")
			return
		
		logging.getLogger(__name__).debug("Writing results to path: %s", result)

		trt = formatting.format_timecode_as_duration(sum(r.runtime_range.duration for r in self._reel_info_list)) if self._reel_info_list else "0:00"

		try:
			with open(result, "w") as handle_export:

				print(formatting.format_trim_list_to_csv(self._reel_info_list), file=handle_export)
				print("Total Runtime: " + trt, file=handle_export)

		except Exception as e:
			logging.getLogger(__name__).error("Error writing results: %s", e, exc_info=True)
		else:
			logging.getLogger(__name__).info("Succesfully wrote results to: %s", result)