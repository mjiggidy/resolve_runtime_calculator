PATH_WORKFLOW_INTEGRATION_PLUGINS = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins"
PACKAGE_ID = "com.glowingpixel.runtimecalculator"

import sys, pathlib

PATH_LIB = pathlib.Path(PATH_WORKFLOW_INTEGRATION_PLUGINS, PACKAGE_ID, "lib")

if not pathlib.Path(PATH_LIB).is_dir():

	print("Required library path not found: ", PATH_LIB, file=sys.stderr)
	sys.exit(1)

if str(PATH_LIB) not in sys.path:
	sys.path.insert(0, str(PATH_LIB))

from runtime_calculator import __main__

try:
	__main__.main()
except Exception as e:
	print(f"Quit unexpectedly: {str(e)}", file=sys.stderr)
	sys.exit(1)