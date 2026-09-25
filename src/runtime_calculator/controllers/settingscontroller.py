from ..gui import wnd_settings
from ..controllers  import mediapoolinput
from ..utils import match_info

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
		window_handle.On[wnd_settings.ID_BTN_SAVE].Clicked               = self._on_save_clicked

		self._match_mediapool_input_controller.register_window_handle(window_handle)
		self._exclude_mediapool_input_controller.register_window_handle(window_handle)

	# Event handling

	def _on_save_clicked(self, event:dict):

		print(self.match_options())

	def _on_match_name_changed(self, event:dict):

		self._window_widget._chk_match_name.Checked = bool(event.get("Text",""))

	def _on_match_folder_changed(self, event:dict):

		self._window_widget._chk_match_folder.Checked = bool(event.get("Text",""))

	def _on_exclude_folder_changed(self, event:dict):

		self._window_widget._chk_exclude_folder.Checked = bool(event.get("Text",""))

	def _on_close(self, event:dict):

		event.get("sender").Hide()

	def set_match_options(self, match_options:match_info.TRTLatestMatchOptions):

		self._window_widget.chk_refresh_project().Checked          = match_options.refresh_project
		self._window_widget.match_mediapool_name_editor().Text     = match_options.match_string
		self._window_widget.match_mediapool_folder_editor().Text   = match_options.match_path
		self._window_widget.exclude_mediapool_folder_editor().Text = match_options.ignore_path

	def match_options(self) -> match_info.TRTLatestMatchOptions:

		return match_info.TRTLatestMatchOptions(
			refresh_project = self._window_widget.chk_refresh_project().Checked,
			match_string    = self._window_widget.match_mediapool_name_editor().Text     if self._window_widget.match_mediapool_name_enabler().Checked     else "",
			match_path      = self._window_widget.match_mediapool_folder_editor().Text   if self._window_widget.match_mediapool_folder_enabler().Checked   else "",
			ignore_path     = self._window_widget.exclude_mediapool_folder_editor().Text if self._window_widget.exclude_mediapool_folder_enabler().Checked else "",
		)