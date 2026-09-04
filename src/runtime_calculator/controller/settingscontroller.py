from .. import dispatcher, ui
from resolvecommon.session import resolve

from ..gui import wnd_settings

class TRTSettingsController:

	def __init__(self):

		self._trt_match_settings_editor = wnd_settings.TRTSettingsEditor(ui)

		self._win_settings = dispatcher.AddWindow({
			"ID": "trt_settings_window",
			"WindowTitle": "Settin's",
			"Events": {},
		}, [self._trt_match_settings_editor.layout()])

		self._setup_window()

		self._win_settings.Show()

	def _setup_window(self):
		print("Yo")

		self._win_settings.On[wnd_settings.ID_TXT_MEDIA_POOL_PATH].ReturnPressed = self.on_media_pool_edited
		#self._win_settings.On["CHECK"].Clicked = self.on_media_pool_edited
		self._win_settings.On[wnd_settings.ID_BTN_USE_CURRENT_FOLDER].Clicked = self.on_use_current_folder

	def on_media_pool_edited(self, event:dict):

		print("Hey")

	def on_use_current_folder(self, event:dict):

		mp = resolve.GetMediaPool()

		self._trt_match_settings_editor._txt_media_pool_folder.Text = mp.GetCurrentFolder().GetName()

		print("Ok")