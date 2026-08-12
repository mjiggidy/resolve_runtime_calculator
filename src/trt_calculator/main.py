from . import wnd_main, select_reels

from . import dispatcher, ui
import logging

MAIN_WINDOW_ID = "com.glowingpixel.trt"

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


def main():

	logging.basicConfig(level=logging.INFO)

	if win:= ui.FindWindow(MAIN_WINDOW_ID):
		
		win.Show()
		win.Raise()
		
		import sys
		sys.exit(0)


	win = dispatcher.AddWindow({
		"ID": MAIN_WINDOW_ID,
		"WindowTitle": "There Can Be Only Run...time",
		"FixedSize": [430,450],
		"Events": {"Close": True},
	}, [trt_main_window.layout()])

	win.On[MAIN_WINDOW_ID].Close = on_close
	win.On[wnd_main.BTN_ID_ADD_LATEST].Clicked = on_add_latest
	win.On[wnd_main.BTN_ID_ADD_SELECTED].Clicked = on_add_selected
	win.On[wnd_main.BTN_ID_CLEAR].Clicked = on_clear

	win.Show()
	dispatcher.RunLoop()



