"""
Binds window events to the application controller.

My thinking is that the controller knows HOW to do stuff,
and the event dispatcher here knows WHEN to do stuff?

Is... is this the way...?  I don't know.  OVERTHINKING.
"""

from __future__ import annotations
import logging, typing

from ..gui import panel_treecontrols, wnd_main, tree_results

if typing.TYPE_CHECKING:
	from .mainwindowcontroller import TRTMainWindowController

class TRTEventDispatcher:
	"""Dispatch events to the controller"""

	def __init__(self, controller:TRTMainWindowController):

		self._controller = controller

	def register_window_handle(self, win_handle:object):
		"""Bind a window handle's events to the controller"""

		# TODO Think about this because... like... the IDs and such

		win_handle.On[wnd_main.ID_WINDOW_MAIN].KeyRelease             = self.on_key_released

		win_handle.On[panel_treecontrols.ID_BTN_ADD_LATEST].Clicked   = self.on_add_latest
		win_handle.On[panel_treecontrols.ID_BTN_ADD_SELECTED].Clicked = self.on_add_selected
		win_handle.On[panel_treecontrols.ID_BTN_CLEAR].Clicked        = self.on_clear

		win_handle.On[wnd_main.ID_BTN_EXPORT].Clicked                 = self.on_export_clicked

		win_handle.On[tree_results.ID_TREE_VIEW].ItemActivated        = self.on_tree_item_activated

	def on_clear(self, event:dict):
		"""User requests clear all results"""

		logging.getLogger(__name__).debug("Got clear reels event.  Modifiers: %s", str(event.get("modifiers",{})))

		if event.get("modifiers",{}).get("ControlModifier",False):
			self._controller.remove_selected_trim_items()

		else:
			self._controller.clear_all()

	def on_add_latest(self, event:dict):
		"""User requests add latest reels"""
		
		logging.getLogger(__name__).debug("Got add-latest event.  Modifiers: %s", str(event.get("modifiers",{})))

		if event.get("modifiers",{}).get("ControlModifier",False):
			self._controller.clear_all()
			
		self._controller.add_latest_reels()

	def on_add_selected(self, event:dict):
		"""User requests add selected clips"""
		
		logging.getLogger(__name__).debug("Got add-selected event.   Modifiers: %s", str(event.get("modifiers",{})))

		if event.get("modifiers",{}).get("ControlModifier",False):
			self._controller.clear_all()

		self._controller.add_selected_reels()

	def on_key_released(self, event:dict):
		"""Handle key release events"""

#		logging.getLogger(__name__).debug("Got key-up event.")

		KEY_DELETE = [16777223, 16777219]
		"""`Delete` and `Backspace` key IDs"""

		# Currently only for "Delete" key in Tree widget
		if event.get("Key") in KEY_DELETE and not event.get("IsAutoRepeat",False) and event.get("sender").FocusWidget().ID == tree_results.ID_TREE_VIEW:

			logging.getLogger(__name__).debug("Key up indicates remove tree item")
			self._controller.remove_selected_trim_items()

	def on_tree_item_activated(self, event:dict):
		"""Trim item was "activated," find it in MediaPool"""

		logging.getLogger(__name__).debug("Got tree item activated event.")

		self._controller.focus_trim_item_in_media_pool(event["item"])

	def on_export_clicked(self, event:dict):
		"""User requested export"""

		logging.getLogger(__name__).debug("Got export button click event.")

		self._controller.export_results()