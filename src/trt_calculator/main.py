from . import wnd_main, select_reels

from . import dispatcher, ui
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

	trt_main_window.set_busy("Refreshing project...")
	select_reels.refresh_project()

	trt_main_window.set_busy("Loading latest...")
	trt_main_window.add_timeline_info(select_reels.get_latest_reels_from_project())
	trt_main_window.set_ready()

def on_add_selected(event:dict):
	
	logging.getLogger(__name__).info("Selected reels requested")

	trt_main_window.set_busy("Loading selected...")
	trt_main_window.add_timeline_info(select_reels.get_selected_reels())
	trt_main_window.set_ready()

def on_ffoa_edited(event:dict):

	tc_text = trt_main_window.ffoa_trim_text()

	try:
		tc_formatted = str(timecode.Timecode(tc_text.strip().lstrip("-"))).lstrip("0:;")
	except Exception as e:
		tc_formatted = ""
	finally:
		trt_main_window.set_ffoa_trim_text(tc_formatted)

def on_lfoa_edited(event:dict):

	tc_text = trt_main_window.lfoa_trim_text()

	try:
		tc_formatted = str(timecode.Timecode(tc_text.strip().lstrip("-"))).lstrip("0:;")
	except Exception as e:
		tc_formatted = ""
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
		"FixedSize": [375,450],
		"Events": {"Close": True},
	}, [trt_main_window.layout()])

	win.On[MAIN_WINDOW_ID].Close = on_close
	win.On[wnd_main.ID_BTN_ADD_LATEST].Clicked = on_add_latest
	win.On[wnd_main.ID_BTN_ADD_SELECTED].Clicked = on_add_selected
	win.On[wnd_main.ID_BTN_CLEAR].Clicked = on_clear

	#win.On[wnd_main.ID_TXT_TRIM_FFOA].EditingFinished = on_ffoa_changed
	win.On[wnd_main.ID_TXT_TRIM_FFOA].EditingFinished  = on_ffoa_edited
	win.On[wnd_main.ID_TXT_TRIM_LFOA].EditingFinished  = on_lfoa_edited

	win.Show()
	dispatcher.RunLoop()