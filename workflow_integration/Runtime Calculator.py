import sys, pathlib, logging
from logging.handlers import RotatingFileHandler

PATH_WORKFLOW_INTEGRATION_PLUGINS = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
PACKAGE_ID="com.glowingpixel.runtimecalculator"

PATH_RES = pathlib.Path(PATH_WORKFLOW_INTEGRATION_PLUGINS, PACKAGE_ID)
PATH_LIB = PATH_RES / "lib"
PATH_LOG = PATH_RES / "logs" / "rtc_log.log"

logging.basicConfig(level=logging.DEBUG)

try:
	PATH_LOG.parent.mkdir(parents=True, exist_ok=True)
except Exception as e:
	logging.getLogger(__name__).error("Could not create log path: %s", e, exc_info=True)
else:
	logging.getLogger(__name__).addHandler(RotatingFileHandler(str(PATH_LOG), maxBytes=128 * 1024, backupCount=5))

logging.getLogger(__name__).info("Hello from %s", __file__)

if not pathlib.Path(PATH_LIB).is_dir():

	logging.getLogger(__name__).critical("Required library path not found: ", PATH_LIB, file=sys.stderr)
	sys.exit(1)

if str(PATH_LIB) not in sys.path:
	sys.path.insert(0, str(PATH_LIB))

from trt_calculator.main import main

main()