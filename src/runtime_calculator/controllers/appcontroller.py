import logging

from .. import dispatcher, ui

from ..gui import wnd_main, wnd_settings
from ..controllers import mainwindowcontroller, settingscontroller
from ..utils import trim_info, marker_info, match_info, window_info

class TRTApplicationController:

	def __init__(
		self,
		/,
		match_options :match_info.TRTLatestMatchOptions,
		trim_options  :trim_info.TRTTrimOptions,
		marker_options:marker_info.TRTMarkerOptions,
		window_options:window_info.TRTMainWindowOptions,
	):

		# Main Window

		self._main_widget     = wnd_main.TRTMainWidget(
			ui,
			show_nag_link=window_options.show_nag_link
		)

		self._main_controller = mainwindowcontroller.TRTMainWindowController(
			self._main_widget,
			match_options=match_options,
			trim_options=trim_options,
			marker_options=marker_options,
		)
		
		self._main_window = dispatcher.AddWindow({
			"ID": wnd_main.ID_WINDOW_MAIN,
			"WindowTitle": window_options.main_window_title,
			"FixedSize": [360,500],
			"Events": {"Close": True, "KeyRelease": True},
		}, [self._main_widget.layout()])

		self._main_window.On[wnd_main.ID_WINDOW_MAIN].Close    = self._on_mainwindow_close
		self._main_window.On[wnd_main.ID_BTN_SETTINGS].Clicked = self._on_settings_requested

		self._main_controller.register_window_handle(self._main_window)

		# Settings Window

		self._settings_widget        = wnd_settings.TRTSettingsWindow(ui)
		self._settings_controller    = settingscontroller.TRTSettingsController(self._settings_widget)
		self._settings_window = dispatcher.AddWindow({
			"ID": wnd_settings.ID_WINDOW_SETTINGS,
			"WindowTitle": "Settings",
			"FixedSize": [420,350],
			"Events": {"Close": True},
		}, [self._settings_widget.layout()])

		self._settings_window.On[wnd_settings.ID_BTN_SAVE].Clicked   = self._on_settings_saved
		self._settings_window.On[wnd_settings.ID_BTN_CANCEL].Clicked = self._on_settings_cancel

		self._settings_controller.register_window_handle(self._settings_window)

		# Launch dat winder
		
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