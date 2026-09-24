"""
Deals with selecting reels.  Only gonna work for meeeee for now!
"""

from __future__ import annotations
import re, logging, typing

from .folders import get_folder_from_path, get_clips_from_folder_by_type
from ..utils import match_info

from resolvecommon.session import resolve

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

def get_latest_from_project(match_options:match_info.TRTLatestMatchOptions) -> list[bmd.MediaPoolItem]:
	"""Determine the latest things"""

	latest_per_part:dict[str, tuple[str, bmd.MediaPoolItem]] = dict()

	if match_options.match_path:
		logging.getLogger(__name__).debug("Search for user-specified folder %s", match_options.match_path)

	else:
		logging.getLogger(__name__).debug("Using root folder by default")

	base_folder   = get_folder_from_path( match_options.match_path, mp.GetRootFolder()) if  match_options.match_path else mp.GetRootFolder()
	ignore_folder = None

	try:
		ignore_folder = get_folder_from_path(match_options.ignore_path, mp.GetRootFolder()) if match_options.ignore_path else None

	except Exception as e:
		logging.getLogger(__name__).error("Not ignoring folder at path %s: %s", match_options.ignore_path, e, exc_info=True)

	else:
		logging.getLogger(__name__).debug("Using ignored folder %s", ignore_folder.GetName())

	for item in get_clips_from_folder_by_type(base_folder, recursive=True, ignore_folder=ignore_folder):

		match = match_options.match_pattern.search(item.GetName())

		if not match:
			
			logging.getLogger(__name__).debug("Not matched: %s", item.GetName())
			continue

		version_parsed = [int(v) if v.isdecimal() else v for v in re.split(r"[^0-9]+", match.group("version"))]
		
		if match.group("part") not in latest_per_part or latest_per_part[match.group("part")][0] < version_parsed:
			latest_per_part[match.group("part")] = (version_parsed, item)

	return [item[1] for item in latest_per_part.values()]

def get_selected_media_pool_items() -> list[bmd.MediaPoolItem]:
	"""Return selected media pool clips"""
	
	return mp.GetSelectedClips() or []

def focus_media_pool_item(media_pool_item:object):
	"""Select a given media pool item"""

	if not mp.SetSelectedClip(media_pool_item):
		raise RuntimeError(f"Could not focus {media_pool_item.GetName()}")