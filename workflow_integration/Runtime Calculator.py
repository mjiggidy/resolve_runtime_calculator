import sys, pathlib, logging, json
from logging.handlers import RotatingFileHandler

PATH_WORKFLOW_INTEGRATION_PLUGINS = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
PACKAGE_ID="com.glowingpixel.runtimecalculator"

PATH_RES = pathlib.Path(PATH_WORKFLOW_INTEGRATION_PLUGINS, PACKAGE_ID)
PATH_LIB = PATH_RES / "lib"
PATH_CFG = PATH_RES / "config" / "rtc_config.json"
PATH_LOG = PATH_RES / "logs" / "rtc_log.log"

# Set up logging

logging.basicConfig(level=logging.DEBUG)

try:
	PATH_LOG.parent.mkdir(parents=True, exist_ok=True)

except Exception as e:
	logging.getLogger(__name__).error("Could not create log path: %s", e, exc_info=True)

else:
	file_handler = RotatingFileHandler(str(PATH_LOG), maxBytes=128 * 1024, backupCount=5)
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
	with open(PATH_CFG) as json_config:
		user_config = json.load(json_config)
		logging.getLogger(__name__).debug("Loaded saved config from %s: %s", PATH_CFG, user_config)

except json.JSONDecodeError as e:
	logging.getLogger(__name__).error("Error decoding %s: %s", PATH_CFG, e, exc_info=True)
	pass
except FileNotFoundError:
	logging.getLogger(__name__).debug("No config file found at %s. To The Defaults!", PATH_CFG)
	pass
except Exception as e:
	logging.getLogger(__name__).error("Strange error accessing %s: %s", PATH_CFG, e, exc_info=True)
	pass

from trt_calculator.main import main

# Call main!
session_config = main(**user_config)

# Save config to disk

try:

	with open(PATH_CFG, "w") as json_file:
		json.dump({
			"use_ffoa_marker": session_config.use_ffoa_marker,
			"use_lfoa_marker": session_config.use_lfoa_marker,
			"trim_from_head" : str(session_config.trim_from_head),
			"trim_from_tail" : str(session_config.trim_from_tail),

		}, json_file)

		logging.getLogger(__name__).debug("Wrote config to %s: %s", PATH_CFG, session_config)

except Exception as e:
	logging.getLogger(__name__).error("Strange error writing %s: %s", PATH_CFG, e, exc_info=True)
	pass