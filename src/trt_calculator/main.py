"""
Main app controller for the thing
"""

import logging, timecode

from . import dispatcher, ui, DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM, PROJECT_FRAME_RATE
from . import trim_info, wnd_main, select_reels, formatting

MAIN_WINDOW_ID    = "com.glowingpixel.runtimecalculator"
MAIN_WINDOW_TITLE = "Runtime Calculator"

DEFAULT_TRIM_OPTIONS = trim_info.TRTTrimOptions(
	trim_from_head  = timecode.Timecode(DEFAULT_HEAD_TRIM, rate=PROJECT_FRAME_RATE),
	trim_from_tail  = timecode.Timecode(DEFAULT_TAIL_TRIM, rate=PROJECT_FRAME_RATE),
	use_ffoa_marker = True,
	use_lfoa_marker = False,
)

class TRTMainApplication:

	def __init__(
		self,
		trim_from_head:str   = DEFAULT_HEAD_TRIM,
		trim_from_tail:str   = DEFAULT_TAIL_TRIM,
		use_ffoa_marker:bool = True,
		use_lfoa_marker:bool = True,
		project_rate:int     = 24
	):

		self._reel_info_list:list[trim_info.TRTTrimInfo] = []
		"""Data model list of individual clip trim info"""

		self._trt_main_window = wnd_main.TRTMainWindow(ui)
		"""Main window controller"""

		self._current_trim_options = trim_info.TRTTrimOptions(
			trim_from_head  = timecode.Timecode(trim_from_head, rate=project_rate),
			trim_from_tail  = timecode.Timecode(trim_from_tail, rate=project_rate),
			use_ffoa_marker = use_ffoa_marker,
			use_lfoa_marker = use_lfoa_marker,
		)
		"""Currently-active trim options"""

		# Setup main window controller
		self._trt_main_window.set_ffoa_trim_text(formatting.format_timecode_as_duration(self._current_trim_options.trim_from_head))
		self._trt_main_window.set_lfoa_trim_text(formatting.format_timecode_as_duration(self._current_trim_options.trim_from_tail))
		self._trt_main_window.set_use_ffoa_marker(self._current_trim_options.use_ffoa_marker)
		self._trt_main_window.set_use_lfoa_marker(self._current_trim_options.use_lfoa_marker)

		# Add mainwindow to  UIDispatcher
		win = self._setup_window()
		win.Show()
		dispatcher.RunLoop()

	def _setup_window(self) -> object:

		if win:= ui.FindWindow(MAIN_WINDOW_ID):

			win.Show()
			win.Raise()
			
			import sys
			sys.exit(0)

		# Use trim options if passsed, otherwise use the defaults
		
		win = dispatcher.AddWindow({
			"ID": MAIN_WINDOW_ID,
			"WindowTitle": MAIN_WINDOW_TITLE,
			"FixedSize": [360,500],
			"Events": {"Close": True},
		}, [self._trt_main_window.layout()])

		win.On[MAIN_WINDOW_ID].Close                       = self.on_close

		win.On[wnd_main.ID_BTN_ADD_LATEST].Clicked         = self.on_add_latest
		win.On[wnd_main.ID_BTN_ADD_SELECTED].Clicked       = self.on_add_selected
		win.On[wnd_main.ID_BTN_CLEAR].Clicked              = self.on_clear

		win.On[wnd_main.ID_TXT_TRIM_FFOA].EditingFinished  = self.on_ffoa_edited
		win.On[wnd_main.ID_TXT_TRIM_LFOA].EditingFinished  = self.on_lfoa_edited

		return win

	def current_trim_options(self) -> trim_info.TRTTrimOptions:

		return self._current_trim_options

	def update_trim_options_from_window(self) -> trim_info.TRTTrimOptions:

		self._current_trim_options = trim_info.TRTTrimOptions(
			trim_from_head = timecode.Timecode(self._trt_main_window.ffoa_trim_text(), rate=PROJECT_FRAME_RATE),
			trim_from_tail = timecode.Timecode(self._trt_main_window.lfoa_trim_text(), rate=PROJECT_FRAME_RATE),
			use_ffoa_marker = self._trt_main_window.use_ffoa_marker(),
			use_lfoa_marker = self._trt_main_window.use_lfoa_marker(),
		)

		return self._current_trim_options

	def add_trimmed_item_info(self, trimmed_item_info:trim_info.TRTTrimInfo):

		logging.getLogger(__name__).debug("Adding info for %s", trimmed_item_info.media_pool_name)

		self._reel_info_list.append(trimmed_item_info)
		self._trt_main_window.add_timeline_info(trimmed_item_info)

		trt = formatting.format_timecode_as_duration(
			sum(r.runtime_range.duration for r in self._reel_info_list)
		) if self._reel_info_list else None

		self._trt_main_window.set_total_runtime(trt)

	###
	# Event handlers
	###

	def on_close(self, event:dict):
		"""Window is closing"""

		# Update options for later writing to disk
		self.update_trim_options_from_window()

		logging.getLogger(__name__).info("Window is closing.  And hey -- thanks.")
		dispatcher.ExitLoop(0)

	def on_clear(self, event:dict):

		logging.getLogger(__name__).info("Clearing reel info")

		self._trt_main_window.set_busy("Clearing...")

		self._reel_info_list.clear()

		self._trt_main_window.clear_timeline_info()
		self._trt_main_window.set_total_runtime()

		self._trt_main_window.set_ready("Cleared")

	def on_add_latest(self, event:dict):
		
		logging.getLogger(__name__).info("Latest reels requested")


		self._trt_main_window.set_busy("Refreshing project...")
		select_reels.refresh_project()

		self._trt_main_window.set_busy("Loading latest...")

		trim_options = self.update_trim_options_from_window()

		trimmed_reels = []
		skipped_reels = []

		for clip in select_reels.get_latest_reels_from_project():

			try:
				trimmed_reels.append(trim_info.TRTTrimInfo(clip, trim_options))

			except Exception as e:
				
				logging.getLogger(__name__).error("Error adding %s: %s", clip.GetName(), e, exc_info=True)
				skipped_reels.append((clip, str(e)))

		for trimmed_reel_info in sorted(trimmed_reels, key=lambda r: formatting.format_string_for_natural_sort(r.media_pool_name)):
			self.add_trimmed_item_info(trimmed_reel_info)

		status_messages = [f"{len(self._reel_info_list)} Reel{'' if len(self._reel_info_list) == 1 else 's'}"]

		if skipped_reels:
			status_messages.append(f"Skipped {len(skipped_reels)}")

		self._trt_main_window.set_ready(", ".join(status_messages))

	def on_add_selected(self, event:dict):
		
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

		status_messages = [f"{len(self._reel_info_list)} Reel{'' if len(self._reel_info_list) == 1 else 's'}"]

		if skipped_reels:
			status_messages.append(f"Skipped {len(skipped_reels)}")

		self._trt_main_window.set_ready(", ".join(status_messages))

	def on_ffoa_edited(self, event:dict):
		"""Validate FFOA trim amount"""

		tc_text = self._trt_main_window.ffoa_trim_text().strip().lstrip("-")

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=PROJECT_FRAME_RATE)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=PROJECT_FRAME_RATE))
		finally:
			self._trt_main_window.set_ffoa_trim_text(tc_formatted)

	def on_lfoa_edited(self, event:dict):
		"""Validate LFOA trim amount"""

		tc_text = self._trt_main_window.lfoa_trim_text().strip().lstrip("-")

		try:
			tc_formatted = formatting.format_timecode_as_duration(
				formatting.format_string_as_timecode(tc_text, timecode_rate=PROJECT_FRAME_RATE)
			)
		except Exception as e:
			tc_formatted = formatting.format_timecode_as_duration(timecode.Timecode("0", rate=PROJECT_FRAME_RATE))
		finally:
			self._trt_main_window.set_lfoa_trim_text(tc_formatted)