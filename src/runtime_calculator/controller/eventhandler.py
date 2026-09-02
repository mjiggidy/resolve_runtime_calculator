from __future__ import annotations
import logging, typing

from ..gui import btns_treecontrols, wnd_main, tree_results, trim_controls

if typing.TYPE_CHECKING:
	from .appcontroller import TRTMainApplication

class TRTEventDispatcher:
	"""Dispatch events to the controller"""

	def __init__(self, controller:TRTMainApplication, window_handle:object|None=None):

		self._controller = controller

		if window_handle:

			self._attach_handlers(window_handle)

	def _attach_handlers(self, win_handle:object):
		"""Attach listeners"""

		win_handle.On[wnd_main.ID_WINDOW_MAIN].Close                   = self.on_close

		win_handle.On[btns_treecontrols.ID_BTN_ADD_LATEST].Clicked         = self.on_add_latest
		win_handle.On[btns_treecontrols.ID_BTN_ADD_SELECTED].Clicked       = self.on_add_selected
		win_handle.On[btns_treecontrols.ID_BTN_CLEAR].Clicked              = self.on_clear

		win_handle.On[trim_controls.ID_TXT_TRIM_FFOA].EditingFinished  = self.on_ffoa_edited
		win_handle.On[trim_controls.ID_TXT_TRIM_LFOA].EditingFinished  = self.on_lfoa_edited

		win_handle.On[wnd_main.ID_WINDOW_MAIN].KeyRelease              = self.on_key_released
		win_handle.On[tree_results.ID_TREE_VIEW].ItemActivated         = self.on_tree_item_activated

	def on_close(self, event:dict):
		"""Window is closing"""

		logging.getLogger(__name__).debug("Got window close event.")

		self._controller.close_window()

	def on_clear(self, event:dict):
		"""User requests clear all results"""

		logging.getLogger(__name__).debug("Got clear reels event.")

		self._controller.clear_all()

	def on_add_latest(self, event:dict):
		"""User requests add latest reels"""
		
		logging.getLogger(__name__).debug("Got add-latest event.")

		self._controller.add_latest_reels()

	def on_add_selected(self, event:dict):
		"""User requests add selected clips"""
		
		logging.getLogger(__name__).debug("Got add-selected event.")

		self._controller.add_selected_reels()

	def on_ffoa_edited(self, event:dict):
		"""Validate FFOA trim amount"""

		logging.getLogger(__name__).debug("Got validate-ffoa event.")

		self._controller.validate_ffoa_trim_amount()

	def on_lfoa_edited(self, event:dict):
		"""Validate LFOA trim amount"""

		logging.getLogger(__name__).debug("Got validate-lfoa event.")

		self._controller.validate_lfoa_trim_amount()

	def on_key_released(self, event:dict):
		"""Handle key release events"""

		logging.getLogger(__name__).debug("Got key-up event: %s", event)

		KEY_DELETE = 16777223
		"""`Delete` key ID"""

		print("Focus widget", event.get("sender").FocusWidget().ID)

		# Currently only for "Delete" key in Tree widget
		if event.get("Key") == KEY_DELETE and event.get("IsAutoRepeat",False) == False and event.get("sender").FocusWidget().ID == tree_results.ID_TREE_VIEW:

			logging.getLogger(__name__).debug("Key up indicates remove tree item")
			self._controller.remove_selected_trim_items()

	def on_tree_item_activated(self, event:dict):
		"""Trim item was "activated," find it in MediaPool"""

		logging.getLogger(__name__).debug("Got tree item activated event.")

		self._controller.focus_trim_item_in_media_pool(event["item"])