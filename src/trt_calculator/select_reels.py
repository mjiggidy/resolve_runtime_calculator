import re, logging

import timecode
from resolvecommon.session import resolve
from resolvecommon.folders import get_folder_from_path, get_clips_from_folder_by_type
from resolvecommon.versioning import PAT_REEL_NAME, get_latest_reel_version
from resolvecommon.itemtypes import ItemTypes

from .reel_info import ReelInfo


REELS_FOLDER_PATH = "00 REELS"
PAT_REEL_FOLDER  = re.compile(r"^\s*REEL (?P<reel_number>\d+)\s*(?P<reel_description>.+)?", re.I)

pm   = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
mp   = proj.GetMediaPool()

def refresh_project():

	logging.getLogger(__name__).info("Refreshing folders...")
	mp.RefreshFolders()

def get_latest_reels_from_project() -> list[ReelInfo]:
	"""Load latest version of each reel"""

	refresh_project()

	logging.getLogger(__name__).info("Getting reels folder...")
	reels_folder = get_folder_from_path(REELS_FOLDER_PATH, mp.GetRootFolder())

	logging.getLogger(__name__).info("Getting timelines from reel folders...")
	
	latest_reels = []
	
	for reel_folder in reels_folder.GetSubFolderList():
		
		reel_folder_match = PAT_REEL_FOLDER.match(reel_folder.GetName())

		if not reel_folder_match:
			
			logging.getLogger(__name__).debug("Skipping non-reel folder %s", reel_folder.GetName())
			continue
		
		timelines_in_folder = []
		
		for timeline_in_folder in get_clips_from_folder_by_type(reel_folder, clip_types=[ItemTypes.TIMELINE], recursive=True):
			
			timeline_match = PAT_REEL_NAME.match(timeline_in_folder.GetName())

			if not timeline_match or not timeline_match.group("reel_number") == reel_folder_match.group("reel_number"):
				
				logging.getLogger(__name__).debug("Skipping non-reel timeline: %s", timeline_in_folder.GetName())
				continue
			
			timelines_in_folder.append(timeline_in_folder)

		latest_reel = get_latest_reel_version(timelines_in_folder)

		if latest_reel:
			latest_reels.append(ReelInfo(latest_reel))

	return sorted(latest_reels, key=lambda r: r.reel_number)

def get_selected_reels() -> list[ReelInfo]:
	
	clips = mp.GetSelectedClips()

	if not clips:
		return []
	
	return [ReelInfo(clip) for clip in clips]