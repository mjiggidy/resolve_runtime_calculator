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

	app = appcontroller.TRTApplicationController(launch_settings)

	# Save config to disk
	user_config_manager.write_user_config(app.trim_options(), app.match_options(),app.marker_options(), launch_settings)

if __name__ == "__main__":
	main()