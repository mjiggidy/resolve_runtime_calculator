from . import wnd_main, select_reels, reel_info

from . import dispatcher, ui, DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM
from .formatting import format_timecode_as_duration
import logging, timecode

MAIN_WINDOW_ID = "com.glowingpixel.trt"
MAIN_WINDOW_TITLE = "Runtime Calculator"

trt_main_window = wnd_main.TRTMainWindow(ui)

def on_close(event:dict):
	
	logging.getLogger(__name__).info("Goodbye.  And hey -- thanks.")
	dispatcher.ExitLoop(0)

def on_clear(event:dict):

	trt_main_window.set_busy("Clearing...")
	trt_main_window.clear_timeline_info()
	trt_main_window.set_ready("Cleared")

def on_add_latest(event:dict):
	
	logging.getLogger(__name__).info("Latest reels requested")

	trim_head = timecode.Timecode(trt_main_window.ffoa_trim_text())
	trim_tail = timecode.Timecode(trt_main_window.lfoa_trim_text())

	trt_main_window.set_busy("Refreshing project...")
	select_reels.refresh_project()

	trt_main_window.set_busy("Loading latest...")

	trimmed_reels = []

	for clip in select_reels.get_latest_reels_from_project():
		trimmed_reels.append(reel_info.ReelInfo(
			clip,
			trim_head,
			trim_tail,
		))

	for trimmed_reel in trimmed_reels:
		trt_main_window.add_timeline_info(trimmed_reel)

	trt_main_window.set_ready()

def on_add_selected(event:dict):
	
	logging.getLogger(__name__).info("Selected reels requested")

	trim_head = timecode.Timecode(trt_main_window.ffoa_trim_text())
	trim_tail = timecode.Timecode(trt_main_window.lfoa_trim_text())

	trt_main_window.set_busy("Loading selected...")

	for clip in select_reels.get_selected_reels():
		trt_main_window.add_timeline_info(reel_info.ReelInfo(clip, trim_head, trim_tail))

	trt_main_window.set_ready()

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