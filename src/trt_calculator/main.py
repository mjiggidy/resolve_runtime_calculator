from . import trim_info, wnd_main, select_reels

from . import dispatcher, ui, DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM
from .formatting import format_timecode_as_duration, format_string_for_natural_sort
from .trim_info import TRTTrimInfo
from .trim_options import TRTTrimOptions
import logging, timecode

MAIN_WINDOW_ID = "com.glowingpixel.trt"
MAIN_WINDOW_TITLE = "Runtime Calculator"

trt_main_window = wnd_main.TRTMainWindow(ui)
reel_infos:list[TRTTrimInfo] = []

def get_trim_options_from_window():

	return TRTTrimOptions(
		trim_from_head = timecode.Timecode(trt_main_window.ffoa_trim_text()),
		trim_from_tail = timecode.Timecode(trt_main_window.lfoa_trim_text()),
		use_ffoa_marker = trt_main_window.use_ffoa_marker(),
		use_lfoa_marker = trt_main_window.use_lfoa_marker(),
	)

def add_trimmed_item_info(trimmed_item_info:TRTTrimInfo):

	logging.getLogger(__name__).debug("Adding info for %s", trimmed_item_info.media_pool_name)

	reel_infos.append(trimmed_item_info)
	trt_main_window.add_timeline_info(trimmed_item_info)

	trt = format_timecode_as_duration(
		sum(r.runtime_range.duration for r in reel_infos)
	) if reel_infos else None

	trt_main_window.set_total_runtime(trt)


def on_close(event:dict):
	
	logging.getLogger(__name__).info("Goodbye.  And hey -- thanks.")
	dispatcher.ExitLoop(0)

def on_clear(event:dict):

	logging.getLogger(__name__).info("Clearing reel info")

	trt_main_window.set_busy("Clearing...")

	reel_infos.clear()

	trt_main_window.clear_timeline_info()
	trt_main_window.set_total_runtime()

	trt_main_window.set_ready("Cleared")

def on_add_latest(event:dict):
	
	logging.getLogger(__name__).info("Latest reels requested")


	trt_main_window.set_busy("Refreshing project...")
	select_reels.refresh_project()

	trt_main_window.set_busy("Loading latest...")

	trim_options = get_trim_options_from_window()

	trimmed_reels = []
	skipped_reels = []

	for clip in select_reels.get_latest_reels_from_project():

		try:
			trimmed_reels.append(trim_info.TRTTrimInfo(clip, trim_options))

		except Exception as e:
			
			logging.getLogger(__name__).error("Error adding %s: %s", clip.GetName(), e, exc_info=True)
			skipped_reels.append((clip, str(e)))

	for trimmed_reel_info in sorted(trimmed_reels, key=lambda r: format_string_for_natural_sort(r.mediapool_name)):
		add_trimmed_item_info(trimmed_reel_info)

	status_messages = [f"{len(reel_infos)} Reel{'' if len(reel_infos) == 1 else 's'}"]

	if skipped_reels:
		status_messages.append(f"Skipped {len(skipped_reels)}")

	trt_main_window.set_ready(", ".join(status_messages))

def on_add_selected(event:dict):
	
	logging.getLogger(__name__).info("Selected reels requested")


	trt_main_window.set_busy("Loading selected...")

	trim_options = get_trim_options_from_window()

	trimmed_reels = []
	skipped_reels = []

	for clip in select_reels.get_selected_reels():

		try:
			trimmed_reels.append(trim_info.TRTTrimInfo(clip, trim_options))

		except Exception as e:
			
			logging.getLogger(__name__).error("Error adding %s: %s", clip.GetName(), e, exc_info=True)
			skipped_reels.append((clip, str(e)))

	for trimmed_reel_info in sorted(trimmed_reels, key=lambda r: format_string_for_natural_sort(r.mediapool_name)):
		add_trimmed_item_info(trimmed_reel_info)

	status_messages = [f"{len(reel_infos)} Reel{'' if len(reel_infos) == 1 else 's'}"]

	if skipped_reels:
		status_messages.append(f"Skipped {len(skipped_reels)}")

	trt_main_window.set_ready(", ".join(status_messages))

def on_ffoa_edited(event:dict):
	"""Validate FFOA trim amount"""

	tc_text = trt_main_window.ffoa_trim_text().strip().lstrip("-")

	try:
		tc_formatted = format_timecode_as_duration(timecode.Timecode(tc_text))
	except Exception as e:
		tc_formatted = format_timecode_as_duration(timecode.Timecode("0"))
	finally:
		trt_main_window.set_ffoa_trim_text(tc_formatted)

def on_lfoa_edited(event:dict):
	"""Validate LFOA trim amount"""

	tc_text = trt_main_window.lfoa_trim_text().strip().lstrip("-")

	try:
		tc_formatted = format_timecode_as_duration(timecode.Timecode(tc_text))
	except Exception as e:
		tc_formatted = format_timecode_as_duration(timecode.Timecode("0"))
	finally:
		trt_main_window.set_lfoa_trim_text(tc_formatted)
	

def main():

	logging.basicConfig(level=logging.INFO)

	if win:= ui.FindWindow(MAIN_WINDOW_ID):
		
		win.Show()
		win.Raise()
		
		import sys
		sys.exit(0)

	win = dispatcher.AddWindow({
		"ID": MAIN_WINDOW_ID,
		"WindowTitle": MAIN_WINDOW_TITLE,
		"FixedSize": [360,500],
		"Events": {"Close": True},
	}, [trt_main_window.layout()])

	trt_main_window.set_ffoa_trim_text(format_timecode_as_duration(DEFAULT_HEAD_TRIM))
	trt_main_window.set_lfoa_trim_text(format_timecode_as_duration(DEFAULT_TAIL_TRIM))

	win.On[MAIN_WINDOW_ID].Close = on_close
	win.On[wnd_main.ID_BTN_ADD_LATEST].Clicked = on_add_latest
	win.On[wnd_main.ID_BTN_ADD_SELECTED].Clicked = on_add_selected
	win.On[wnd_main.ID_BTN_CLEAR].Clicked = on_clear

	#win.On[wnd_main.ID_TXT_TRIM_FFOA].EditingFinished = on_ffoa_changed
	win.On[wnd_main.ID_TXT_TRIM_FFOA].EditingFinished  = on_ffoa_edited
	win.On[wnd_main.ID_TXT_TRIM_LFOA].EditingFinished  = on_lfoa_edited

	win.Show()
	dispatcher.RunLoop()