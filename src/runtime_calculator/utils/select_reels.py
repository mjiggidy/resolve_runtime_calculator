"""
Deals with selecting reels.  Only gonna work for meeeee for now!
"""

from __future__ import annotations
import re, logging, typing

from .folders import get_folder_from_path, get_clips_from_folder_by_type

from resolvecommon.session import resolve
#from resolvecommon.versioning import PAT_REEL_NAME, get_latest_reel_version
#from resolvecommon.itemtypes import ItemTypes

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as bmd

REELS_FOLDER_PATH = "00 REELS"
PAT_REEL_FOLDER  = re.compile(r"^\s*REEL (?P<reel_number>\d+)\s*(?P<reel_description>.+)?", re.I)

pm   = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
mp   = proj.GetMediaPool()

def refresh_project():

	logging.getLogger(__name__).info("Refreshing folders...")
	mp.RefreshFolders()

def get_latest_from_project(from_folder_path:str, match_pattern:re.Pattern, ignore_path:str="") -> list[bmd.MediaPoolItem]:
	"""Determine the latest things"""

	latest_per_ep:dict[str, tuple[str, bmd.MediaPoolItem]] = dict()

	if from_folder_path:
		logging.getLogger(__name__).debug("Search for user-specified folder %s", from_folder_path)
	else:
		logging.getLogger(__name__).debug("Using root folder by default")

	base_folder:bmd.Folder = get_folder_from_path(from_folder_path, mp.GetRootFolder()) if from_folder_path else mp.GetRootFolder()
	ignore_folder = get_folder_from_path(ignore_path, mp.GetRootFolder()) if ignore_path else None

	logging.getLogger(__name__).debug("Ignored folder is %s", ignore_folder.GetName())

	for item in get_clips_from_folder_by_type(base_folder, recursive=True, ignore_folder=ignore_folder):

		match = match_pattern.search(item.GetName())

		if not match:

			logging.getLogger(__name__).debug("Not matched: %s", item.GetName())
			continue

		version_parsed = [int(v) for v in re.split(r"[^0-9]+", match.group("version"))]
		
		if match.group("ep") not in latest_per_ep or latest_per_ep[match.group("ep")][0] < version_parsed:
			latest_per_ep[match.group("ep")] = (version_parsed, item)

	return [item[1] for item in latest_per_ep.values()]

def get_selected_reels() -> list[object]:
	"""Return selected media pool clips"""
	
	return mp.GetSelectedClips() or []

def focus_reel(media_pool_item:object):
	"""Select a given media pool item"""

	if not mp.SetSelectedClip(media_pool_item):
		raise RuntimeError(f"Could not focus {media_pool_item.GetName()}")