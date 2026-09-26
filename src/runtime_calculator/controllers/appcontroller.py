import logging

from .. import dispatcher, ui

from ..gui import wnd_main, wnd_settings
from ..controllers import mainwindowcontroller, settingscontroller
from ..utils import trim_info, marker_info, match_info

class TRTApplicationController:

	def __init__(self, launch_settings:dict):

		# Main window
		self._main_widget     = wnd_main.TRTMainWidget(
			ui,
			show_nag_link=launch_settings.get("show_nag_link",True)
		)

		self._main_controller = mainwindowcontroller.TRTMainWindowController(
			self._main_widget,
			**launch_settings
		)

		self._settings_widget        = wnd_settings.TRTSettingsWindow(ui)
		self._settings_controller    = settingscontroller.TRTSettingsController(self._settings_widget)

		self._main_window = dispatcher.AddWindow({
			"ID": wnd_main.ID_WINDOW_MAIN,
			"WindowTitle": launch_settings.get("window_title", wnd_main.DEFAULT_WINDOW_TITLE),
			"FixedSize": [360,500],
			"Events": {"Close": True, "KeyRelease": True},
		}, [self._main_widget.layout()])

		self._settings_window = dispatcher.AddWindow({
			"ID": wnd_settings.ID_WINDOW_SETTINGS,
			"WindowTitle": "Settings",
			"FixedSize": [420,350],
			"Events": {"Close": True},
		}, [self._settings_widget.layout()])


		self._main_window.On[wnd_main.ID_WINDOW_MAIN].Close    = self._on_mainwindow_close
		self._main_window.On[wnd_main.ID_BTN_SETTINGS].Clicked = self._on_settings_requested

		self._main_controller.register_window_handle(self._main_window)

		self._settings_window.On[wnd_settings.ID_BTN_SAVE].Clicked   = self._on_settings_saved
		self._settings_window.On[wnd_settings.ID_BTN_CANCEL].Clicked = self._on_settings_cancel

		self._settings_controller.register_window_handle(self._settings_window)

		self._main_window.Show()

		dispatcher.RunLoop()

	# Events handlings

	def _on_mainwindow_close(self, event:dict):

		logging.getLogger(__name__).debug("Window is closing.  And hey -- thanks.")
		dispatcher.ExitLoop(0)

	def _on_settings_requested(self, event:dict):

		logging.getLogger(__name__).debug("Got settings button clicked event")
		self._settings_controller.set_match_options(self._main_controller.match_options())
		self._settings_controller.set_marker_options(self._main_controller.marker_options())
		self._settings_window.Show()

	def _on_settings_saved(self, event:dict):

		logging.getLogger(__name__).debug("Got settings save button clicked event")

		self._main_controller.set_match_options(self._settings_controller.match_options())
		self._main_controller.set_marker_options(self._settings_controller.marker_options())

		self._settings_window.Hide()
		print(self._settings_controller.marker_options())

	def _on_settings_cancel(self, event:dict):

		logging.getLogger(__name__).debug("Got settings cancel button clicked event")
		self._settings_window.Hide()

	# Gettersnsetters

	def trim_options(self) -> trim_info.TRTTrimOptions:

		return self._main_controller.trim_options()

	def marker_options(self) -> marker_info.TRTMarkerOptions:

		return self._settings_controller.marker_options()

	def match_options(self) -> match_info.TRTLatestMatchOptions:

		return self._settings_controller.match_options()