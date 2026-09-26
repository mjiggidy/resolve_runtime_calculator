import json, logging, pathlib, typing
import timecode

from os import PathLike
from . import trim_info, match_info, marker_info, window_info

from .. import DEFAULT_HEAD_TRIM, DEFAULT_TAIL_TRIM, DEFAULT_MATCH_STRING, DEFAULT_FFOA_MARKER_NAME, DEFAULT_LFOA_MARKER_NAME, DEFAULT_WINDOW_TITLE

class ConfigFileManager:
	"""Read and write the config files"""

	def __init__(self, path_user_config:str|PathLike[str]):

		self._path_user_config = pathlib.Path(path_user_config)
		self._user_config      = self.read_user_config()

		logging.getLogger(__name__).debug("Config file manager initiated with path %s", self._path_user_config)

	def user_config(self) -> dict[str, typing.Any]:
		"""Raw user config dict"""

		return self._user_config

	def trim_options(self) -> trim_info.TRTTrimOptions:

		last_tc_rate = self._user_config.get("tc_rate", 24)

		return trim_info.TRTTrimOptions(
			trim_from_head  = timecode.Timecode(self._user_config.get("trim_from_head", DEFAULT_HEAD_TRIM), rate=last_tc_rate),
			trim_from_tail  = timecode.Timecode(self._user_config.get("trim_from_tail", DEFAULT_TAIL_TRIM), rate=last_tc_rate),
			use_ffoa_marker = self._user_config.get("use_ffoa_marker", True),
			use_lfoa_marker = self._user_config.get("use_lfoa_marker", True),
		)

	def match_options(self) -> match_info.TRTLatestMatchOptions:

		return match_info.TRTLatestMatchOptions(
			refresh_project = self._user_config.get("refresh_project", True),
			match_string    = self._user_config.get("match_string", DEFAULT_MATCH_STRING),
			match_path      = self._user_config.get("match_path",""),
			ignore_path     = self._user_config.get("ignore_path",""),
		)

	def marker_options(self) -> marker_info.TRTMarkerOptions:

		return marker_info.TRTMarkerOptions(
			ffoa_marker_name = self._user_config.get("ffoa_marker_name", DEFAULT_FFOA_MARKER_NAME),
			lfoa_marker_name = self._user_config.get("lfoa_marker_name", DEFAULT_LFOA_MARKER_NAME)
		)

	def main_window_options(self) -> window_info.TRTMainWindowOptions:

		return window_info.TRTMainWindowOptions(
			show_nag_link     = self._user_config.get("show_nag_link", True),
			main_window_title = self._user_config.get("window_title", DEFAULT_WINDOW_TITLE)
		)
		
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


	def write_user_config(self, trim_options:trim_info.TRTTrimOptions, match_options:match_info.TRTLatestMatchOptions, marker_options:marker_info.TRTMarkerOptions):
		"""Write user config to disk"""

		self._user_config.update({
			"tc_rate"        : trim_options.trim_from_head.rate,
			"use_ffoa_marker": trim_options.use_ffoa_marker,
			"use_lfoa_marker": trim_options.use_lfoa_marker,
			"trim_from_head" : str(trim_options.trim_from_head),
			"trim_from_tail" : str(trim_options.trim_from_tail),

			"match_string"   : match_options.match_string,
			"match_path"     : match_options.match_path,
			"ignore_path"    : match_options.ignore_path,
			"refresh_project": match_options.refresh_project,

			"ffoa_marker_name": marker_options.ffoa_marker_name,
			"lfoa_marker_name": marker_options.lfoa_marker_name,
		})

		try:

			self._path_user_config.parent.mkdir(parents=True, exist_ok=True)

			with open(self._path_user_config, "w") as json_file:

				json.dump(self._user_config, json_file, indent="\t")
				logging.getLogger(__name__).debug("Wrote config to %s: %s", self._path_user_config, trim_options)

		except Exception as e:
			
			logging.getLogger(__name__).error("Strange error writing %s: %s", self._path_user_config, e, exc_info=True)
			pass