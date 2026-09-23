import json, logging, pathlib, typing

from os import PathLike
from . import trim_info

class ConfigFileManager:
	"""Read and write the config files"""

	def __init__(self, path_user_config:str|PathLike[str]):

		self._path_user_config = pathlib.Path(path_user_config)

		logging.getLogger(__name__).debug("Config file manager initiated with path %s", self._path_user_config)
		
	def read_user_config(self) -> dict[str, typing.Any]:
		"""Read user config from `.json` on disk"""

		user_config = {}

		try:

			self._path_user_config.parent.mkdir(parents=True, exist_ok=True)

			with open(self._path_user_config) as json_config:

				user_config = json.load(json_config)
				logging.getLogger(__name__).debug("Loaded saved config from %s: %s", self._path_user_config, user_config)

		except PermissionError as e:

			logging.getLogger(__name__).error("Error accessing config file path %s: %s", self._path_user_config, e, exc_info=True)
			pass

		except json.JSONDecodeError as e:

			logging.getLogger(__name__).error("Error decoding %s: %s", self._path_user_config, e, exc_info=True)
			pass

		except FileNotFoundError:

			logging.getLogger(__name__).debug("No config file found at %s. To The Defaults!", self._path_user_config)
			pass

		except Exception as e:

			logging.getLogger(__name__).error("Strange error accessing %s: %s", self._path_user_config, e, exc_info=True)
			pass

		return user_config


	def write_user_config(self, trim_options:trim_info.TRTTrimOptions, base_config:dict|None=None):
		"""Write user config to disk"""

		user_config = base_config or {}

		user_config.update({
			"use_ffoa_marker": trim_options.use_ffoa_marker,
			"use_lfoa_marker": trim_options.use_lfoa_marker,
			"trim_from_head" : str(trim_options.trim_from_head),
			"trim_from_tail" : str(trim_options.trim_from_tail),
	#		"match_pattern"  : app._match_pattern.pattern,
	#		"match_path"     : app._match_path,
	#		"ignore_path"    : app._ignore_path,
		})

		try:

			self._path_user_config.parent.mkdir(parents=True, exist_ok=True)

			with open(self._path_user_config, "w") as json_file:

				json.dump(user_config, json_file, indent="\t")
				logging.getLogger(__name__).debug("Wrote config to %s: %s", self._path_user_config, trim_options)

		except Exception as e:
			
			logging.getLogger(__name__).error("Strange error writing %s: %s", self._path_user_config, e, exc_info=True)
			pass