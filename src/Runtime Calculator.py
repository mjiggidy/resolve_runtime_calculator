"""Bootstrap for Resolve"""
import sys, logging

try:
	from resolvecommon.session import bmd, resolve, fusion
except ImportError as e:
	print("Cannot find the Davinci Resolve API.  Please ensure Davinci Resolve Studio is installed and operational.", file=sys.stderr)
	sys.exit(1)

if not resolve:
	print("Cannot connect to Davinci Resolve Studio.  Please ensure it is running, and has scripting enabled.", file=sys.stderr)
	sys.exit(2)

if not fusion:
	print("Cannot connect to Fusion.", file=sys.stderr)
	sys.exit(3)

if __name__ == "__main__":

	from trt_calculator.main import TRTMainApplication
	import json

	PATH_CONFIG = "config.json"

	user_config = {}

	try:
		with open(PATH_CONFIG) as json_config:
			user_config = json.load(json_config)
			print(user_config)

	except json.JSONDecodeError as e:
		logging.getLogger(__name__).error("Error decoding %s: %s", PATH_CONFIG, e, exc_info=True)
		pass
	except FileNotFoundError:
		logging.getLogger(__name__).debug("No config file found at %s. To The Defaults!", PATH_CONFIG)
		pass
	except Exception as e:
		logging.getLogger(__name__).error("Strange error accessing %s: %s", PATH_CONFIG, e, exc_info=True)
		pass

	app = TRTMainApplication(**user_config)

	try:
		session_options = app.current_trim_options()
		with open(PATH_CONFIG, "w") as json_file:
			json.dump({
				"use_ffoa_marker": session_options.use_ffoa_marker,
				"use_lfoa_marker": session_options.use_lfoa_marker,
				"trim_from_head" : str(session_options.trim_from_head),
				"trim_from_tail" : str(session_options.trim_from_tail),

			}, json_file)
			print("K")

	except Exception as e:
		logging.getLogger(__name__).error("Strange error writing %s: %s", PATH_CONFIG, e, exc_info=True)
		pass