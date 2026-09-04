from .abstract_widget import TRTAbstractWidget

ID_TXT_MEDIA_POOL_PATH = "media_pool_path"
ID_BTN_USE_CURRENT_FOLDER = "use_current_folder"

class TRTSettingsEditor(TRTAbstractWidget):
	"""Runtime Calculator settings winder"""

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		self._chk_refresh_project = self._ui.CheckBox({
			"ID": "CHECK",
			"Text": "Refresh project before searching",
			"Checked": True,
			"Events": {"Clicked": True},
		})

		self._chk_limit_media_pool = self._ui.CheckBox({
			"Weight": 0,
			"Text": "Limit to media pool folder:",
			"Checked": True,
			"Events": {},
		})

		self._txt_media_pool_folder = self._ui.LineEdit({
			"ID": ID_TXT_MEDIA_POOL_PATH,
			"PlaceholderText": "Media Pool Path",
			"Text": "/00_REELS",
			"Events": {"ReturnPressed", True},
		})

		self._btn_use_current_folder = self._ui.Button({
			"ID": ID_BTN_USE_CURRENT_FOLDER,
			"Weight": 0,
			"Text": "Use Current Folder",
		})

		self._lay_media_pool = self._ui.HGroup([
			self._chk_limit_media_pool,
			self._txt_media_pool_folder,
			self._btn_use_current_folder,
		])



	def layout(self) -> object:

		return self._ui.VGroup(
			{
				"Weight": 0,
			},
			[
				self._chk_refresh_project,
				self._lay_media_pool,
			]
		)