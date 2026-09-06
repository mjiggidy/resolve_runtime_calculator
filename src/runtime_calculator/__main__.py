import pathlib, logging, json

from runtime_calculator.controller.appcontroller import TRTMainWindowController

from . import ui

#PATH_WORKFLOW_INTEGRATION_PLUGINS = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
#PACKAGE_ID="com.glowingpixel.runtimecalculator"

#PATH_RES = pathlib.Path(PATH_WORKFLOW_INTEGRATION_PLUGINS, PACKAGE_ID)
#PATH_LIB = PATH_RES / "lib"

## Global locations, not yet used
#PATH_CFG_GLOBAL = PATH_RES / "config" / "global_config.json"
#PATH_LOG_GLOBAL = PATH_RES / "logs" / "global_log.log"

# User locations, macOS only
PATH_USER_BASE = pathlib.Path.home() / "Library" / "Application Support" / "GlowingPixel" / "Resolve Runtime Calculator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"

def setup_logging():
	"""Establish logging handlers"""

	from logging.handlers import RotatingFileHandler
	
	PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

	logging.basicConfig(level=logging.DEBUG)

	try:
		PATH_LOG_USER.parent.mkdir(parents=True, exist_ok=True)

	except Exception as e:
		logging.getLogger(__name__).error("Could not create log path: %s", e, exc_info=True)

	else:
		file_handler = RotatingFileHandler(str(PATH_LOG_USER), maxBytes=128 * 1024, backupCount=5)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(logging.Formatter("[%(asctime)s]\t%(levelname)s\t%(name)s\t%(message)s"))
		logging.getLogger().addHandler(file_handler)

	logging.getLogger(__name__).info("Hello from %s", __name__)

def get_user_config() -> dict:
	"""Read user config from `.json` on disk"""

	user_config = {}

	try:

		PATH_CFG_USER.parent.mkdir(parents=True, exist_ok=True)

		with open(PATH_CFG_USER) as json_config:

			user_config = json.load(json_config)
			logging.getLogger(__name__).debug("Loaded saved config from %s: %s", PATH_CFG_USER, user_config)

	except PermissionError as e:

		logging.getLogger(__name__).error("Error accessing config file path %s: %s", PATH_CFG_USER, e, exc_info=True)
		pass

	except json.JSONDecodeError as e:

		logging.getLogger(__name__).error("Error decoding %s: %s", PATH_CFG_USER, e, exc_info=True)
		pass

	except FileNotFoundError:

		logging.getLogger(__name__).debug("No config file found at %s. To The Defaults!", PATH_CFG_USER)
		pass

	except Exception as e:

		logging.getLogger(__name__).error("Strange error accessing %s: %s", PATH_CFG_USER, e, exc_info=True)
		pass

	return user_config

def write_user_config(app:TRTMainWindowController):
	"""Write user config to disk"""

	trim_options = app.update_trim_options_from_window()

	try:

		PATH_CFG_USER.parent.mkdir(parents=True, exist_ok=True)

		with open(PATH_CFG_USER, "w") as json_file:
			json.dump({
				"use_ffoa_marker": trim_options.use_ffoa_marker,
				"use_lfoa_marker": trim_options.use_lfoa_marker,
				"trim_from_head" : str(trim_options.trim_from_head),
				"trim_from_tail" : str(trim_options.trim_from_tail),
			}, json_file)

			logging.getLogger(__name__).debug("Wrote config to %s: %s", PATH_CFG_USER, trim_options)

	except Exception as e:
		logging.getLogger(__name__).error("Strange error writing %s: %s", PATH_CFG_USER, e, exc_info=True)
		pass

def main():

	# If an instance is already running (window is registered with UIDispatcher), 
	# just raise the existing window and get the heck outta there buddy.
	
	from runtime_calculator.gui.wnd_main import ID_WINDOW_MAIN
	if win:= ui.FindWindow(ID_WINDOW_MAIN):
		print("Yep")
		win.Show()
		win.Raise()
		
		import sys
		print("Window instance already running.  There can only be one.", file=sys.stderr)
		sys.exit(0)

	print("Nope")

	setup_logging()

	# Actually do the thing
	app = TRTMainWindowController(**get_user_config())

	# Save config to disk
	write_user_config(app)


if __name__ == "__main__":
	main()