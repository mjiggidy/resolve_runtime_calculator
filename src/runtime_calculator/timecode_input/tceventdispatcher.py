from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
	from . import tcinputcontroller

class TRTTimecodeInputDispatcher:
	"""Dispatch events to the controller"""

	def __init__(self, controller:tcinputcontroller.TRTTimecodeInputController, window_handle:object|None=None):

		self._controller = controller

		if window_handle:
			self.register_window_handle(window_handle)

	def register_window_handle(self, win_handle:object):
		"""Bind a window handle's events to the controller"""

		win_handle.On[self._controller.layout_manager().id()].EditingFinished = self.on_edited

	def on_edited(self, event:dict):

		self._controller.reformat_text()