"""
Deals with selecting reels.  Only gonna work for meeeee for now!
"""

from __future__ import annotations
import logging, typing

from .folders import get_folder_from_path, get_clips_from_folder
from ..utils import match_info, formatting

from resolvecommon.session import resolve

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as bmd
	resolve:bmd.Resolve
	
type ParsedVersion = list[str,int]
"""Parsed, comparible version string"""

EMPTY_PART:str = ""

pm   = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
mp   = proj.GetMediaPool()

def refresh_project():

	logging.getLogger(__name__).info("Refreshing folders...")
	mp.RefreshFolders()

def get_latest_from_project(match_options:match_info.TRTLatestMatchOptions) -> list[bmd.MediaPoolItem]:
	"""Determine the latest things"""

	latest_per_part:dict[str, list[tuple[ParsedVersion, bmd.MediaPoolItem]]] = dict()

	base_folder   = get_folder_from_path(match_options.match_path, mp.GetRootFolder())  if match_options.match_path else mp.GetRootFolder()
	ignore_folder = get_folder_from_path(match_options.ignore_path, mp.GetRootFolder()) if match_options.ignore_path else None

	for item in get_clips_from_folder(base_folder, recursive=True, ignore_folder=ignore_folder):

		match = match_options.match_pattern.search(item.GetName())

		if not match:
			
			logging.getLogger(__name__).debug("Not matched: %s", item.GetName())
			continue

		parsed_part    = match.group("part") if "part" in match.groupdict() else EMPTY_PART

		if "version" in match.groupdict():

			# Return only the latest version for a given part
			
			#parsed_version = [int(v) if v.isdecimal() else v for v in re.split(r"[^0-9]+", match.group("version"))]
			parsed_version = formatting.format_string_for_natural_sort(match.group("version"))	# NOTE: I... guess this would work huh?! Am I crazy?
		
			if parsed_part not in latest_per_part or latest_per_part[parsed_part][0][0] < parsed_version:
				latest_per_part[parsed_part] = [(parsed_version, item)]

		else:

			# No grouping needed as long as it matches
			if EMPTY_PART not in latest_per_part:
				latest_per_part[EMPTY_PART] = []

			latest_per_part[EMPTY_PART].append(([0,0,0], item))

	return [item[1] for items in latest_per_part.values() for item in items]

def get_selected_media_pool_items() -> list[bmd.MediaPoolItem]:
	"""Return selected media pool clips"""
	
	return mp.GetSelectedClips() or []

def focus_media_pool_item(media_pool_item:object):
	"""Select a given media pool item"""

	if not mp.SetSelectedClip(media_pool_item):
		raise RuntimeError(f"Could not focus {media_pool_item.GetName()}")