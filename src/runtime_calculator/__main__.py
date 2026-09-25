import logging, sys

from .utils import paths, logs, user_config
from .controllers import appcontroller
from .gui import wnd_main

from resolvecommon.session import resolve
from . import ui, dispatcher

# User locations, macOS only
PATH_USER_BASE = paths.get_user_base_path()
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

RESOLVE_MINIMUM_VERSION = [21,0,4]

def main():

	# If an instance is already running (window is registered with UIDispatcher), 
	# just raise the existing window and get the heck outta there buddy.

	if win:= ui.FindWindow(wnd_main.ID_WINDOW_MAIN):

		win.Show()
		win.Raise()

		print("Window instance already running.  There can only be one.", file=sys.stderr)
		return

	logs.setup_logging(PATH_LOG_USER)

	try:

		resolve_version = resolve.GetVersion()
		logging.getLogger(__name__).debug("Resolve reports version=%s", resolve_version)

		if RESOLVE_MINIMUM_VERSION > resolve_version:
			raise RuntimeError(f"This plugin requires Resolve version {'.'.join(str(v) for v in RESOLVE_MINIMUM_VERSION)} or newer (got: {'.'.join(str(v) for v in resolve_version)})")

	except Exception as e:

		print("Cannot run: ", str(e), file=sys.stderr)
		return

	# Load in user user config
	user_config_manager = user_config.ConfigFileManager(PATH_CFG_USER)
	launch_settings     = user_config_manager.read_user_config()

	# Actually do the thing
	main_window_widget     = wnd_main.TRTMainWindowWidget(ui, show_nag_link=launch_settings.get("show_nag_link",True))
	main_window_controller = appcontroller.TRTMainWindowController(main_window_widget, **launch_settings)

	main_window_handle = dispatcher.AddWindow({
		"ID": wnd_main.ID_WINDOW_MAIN,
		"WindowTitle": launch_settings.get("window_title", wnd_main.DEFAULT_WINDOW_TITLE),
		"FixedSize": [360,500],
		"Events": {"Close": True, "KeyRelease": True},
	}, [main_window_widget.layout()])

	main_window_handle.On[wnd_main.ID_WINDOW_MAIN].Close = _on_mainwindow_close
	main_window_controller.register_window_handle(main_window_handle)

	main_window_handle.Show()

	# TEMP
	main_window_controller.show_settings_window()

	dispatcher.RunLoop()

	# Save config to disk
	user_config_manager.write_user_config(main_window_widget.trim_controls().trim_options(), launch_settings)

def _on_mainwindow_close(event:dict):

	logging.getLogger(__name__).debug("Window is closing.  And hey -- thanks.")
	dispatcher.ExitLoop(0)


if __name__ == "__main__":
	main()