from ..gui import wnd_settings
from ..controllers  import mediapoolinput

class TRTSettingsController:

	def __init__(self, settings_widget:wnd_settings.TRTSettingsWindow):

		self._window_widget = settings_widget

		self._match_mediapool_input_controller   = mediapoolinput.TRTMediaPoolInputController(self._window_widget.match_mediapool_folder_editor())
		self._exclude_mediapool_input_controller = mediapoolinput.TRTMediaPoolInputController(self._window_widget.exclude_mediapool_folder_editor())

	def register_window_handle(self, window_handle:object):

		window_handle.On[wnd_settings.ID_WINDOW_SETTINGS].Close          = self._on_close
		window_handle.On[wnd_settings.ID_TXT_MATCH_NAME].TextChanged     = self._on_match_name_changed
		window_handle.On[wnd_settings.ID_TXT_MATCH_FOLDER].TextChanged   = self._on_match_folder_changed
		window_handle.On[wnd_settings.ID_TXT_EXCLUDE_FOLDER].TextChanged = self._on_exclude_folder_changed

		self._match_mediapool_input_controller.register_window_handle(window_handle)
		self._exclude_mediapool_input_controller.register_window_handle(window_handle)

	def _on_match_name_changed(self, event:dict):

		self._window_widget._chk_match_name.Checked = bool(event.get("Text",""))

	def _on_match_folder_changed(self, event:dict):

		self._window_widget._chk_match_folder.Checked = bool(event.get("Text",""))

	def _on_exclude_folder_changed(self, event:dict):

		self._window_widget._chk_exclude_folder.Checked = bool(event.get("Text",""))

	def _on_close(self, event:dict):

		event.get("sender").Hide()