import sys, pathlib, logging, json
from logging.handlers import RotatingFileHandler

PATH_WORKFLOW_INTEGRATION_PLUGINS = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
PACKAGE_ID="com.glowingpixel.runtimecalculator"

PATH_RES = pathlib.Path(PATH_WORKFLOW_INTEGRATION_PLUGINS, PACKAGE_ID)
PATH_LIB = PATH_RES / "lib"

# Global locations, not yet used
PATH_CFG_GLOBAL = PATH_RES / "config" / "global_config.json"
PATH_LOG_GLOBAL = PATH_RES / "logs" / "global_log.log"

# User locations, macOS only
PATH_USER_BASE = pathlib.Path.home() / "Library" / "Application Support" / "GlowingPixel" / "Resolve Runtime Calculator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.json"


# Set up logging

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

# Import trt_calculator from its lib path

if not pathlib.Path(PATH_LIB).is_dir():

	logging.getLogger(__name__).critical("Required library path not found: ", PATH_LIB, file=sys.stderr)
	sys.exit(1)

if str(PATH_LIB) not in sys.path:
	sys.path.insert(0, str(PATH_LIB))

# Read in saved config if available

user_config = {}

try:

	PATH_CFG_USER.parent.mkdir(parents=True, exist_ok=True)

	with open(PATH_CFG_USER) as json_config:
		user_config = json.load(json_config)
		logging.getLogger(__name__).debug("Loaded saved config from %s: %s", PATH_CFG_USER, user_config)

except PermissionError as e:
	logging.getLogger(__name__).error("Error writing config file to path %s: %s", PATH_CFG_USER, e, exc_info=True)
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

from trt_calculator.main import TRTMainApplication

# Call main!
app = TRTMainApplication(**user_config)

# Save config to disk

try:

	session_config = app.update_trim_options_from_window()

	PATH_CFG_USER.parent.mkdir(parents=True, exist_ok=True)

	with open(PATH_CFG_USER, "w") as json_file:
		json.dump({
			"use_ffoa_marker": session_config.use_ffoa_marker,
			"use_lfoa_marker": session_config.use_lfoa_marker,
			"trim_from_head" : str(session_config.trim_from_head),
			"trim_from_tail" : str(session_config.trim_from_tail),

		}, json_file)

		logging.getLogger(__name__).debug("Wrote config to %s: %s", PATH_CFG_USER, session_config)

except Exception as e:
	logging.getLogger(__name__).error("Strange error writing %s: %s", PATH_CFG_USER, e, exc_info=True)
	pass