from .abstract_widget import TRTAbstractWidget

ID_WINDOW_SETTINGS    = "win_settings"
ID_CHECK_REFRESH      = "chk_refresh"
ID_CHECK_MATCH_NAME   = "chk_match_name"
ID_TXT_MATCH_NAME     = "txt_match_name"
ID_CHK_MATCH_FOLDER   = "chk_match_folder"
ID_TXT_MATCH_FOLDER   = "txt_match_folder"
ID_CHK_EXCLUDE_FOLDER = "chk_exclude_folder"
ID_TXT_EXCLUDE_FOLDER = "txt_exclude_folder"

TXT_TIP_FONT_POINT_SIZE = 10

class TRTSettingsWindow(TRTAbstractWidget):

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		# Refresh project

		self._chk_refresh = self._ui.CheckBox({
			"ID": ID_CHECK_REFRESH,
			"Text": "Refresh project before adding latest (shared projects only)",
			"Events": {}
		})

		self._chk_match_name = self._ui.CheckBox({
			"ID": ID_CHECK_MATCH_NAME,
			"Weight": 0,
			"Text": "Match Naming Pattern:",
			"MinimumSize": [180,20],
			"Events": {},
		})

		self._lbl_match_name_explained = self._ui.Label({
			"Text": "Specify a naming pattern to match clip names.  Include <code>{part}</code> and <code>{version}</code> tokens as wildcards.  They will be used to determine the latest <code>{version}</code> of each <code>{part}</code>.",
			"WordWrap": True,
			"Font": self._ui.Font({"PointSize": TXT_TIP_FONT_POINT_SIZE}),
			"MinimumSize": [200,50],
		})

		# Match naming pattern

		self._txt_match_name = self._ui.LineEdit({
			"ID": ID_TXT_MATCH_NAME,
			"PlaceholderText": "Match name pattern",
			"Events": {"TextChanged": True},
		})

		self._chk_match_folder = self._ui.CheckBox({
			"ID": ID_CHK_MATCH_FOLDER,
			"Weight": 0,
			"MinimumSize": [180,20],
			"Text": "Start In Media Pool Folder:",
		})

		# Match media pool folder

		self._lbl_match_folder_master = self._ui.Label({
			"Weight": 0,
			"Text": "Master /",
		})

		self._txt_match_folder = self._ui.LineEdit({
			"ID": ID_TXT_MATCH_FOLDER,
			"Events": {"TextEdited": True, "TextChanged": True},
		})

		# Exclude media pool folder

		self._chk_exclude_folder = self._ui.CheckBox({
			"ID": ID_CHK_EXCLUDE_FOLDER,
			"Weight": 0,
			"MinimumSize": [180,20],
			"Text": "Exclude Media Pool Folder:",
		})

		self._lbl_exclude_folder_master = self._ui.Label({
			"Weight": 0,
			"Text": "Master /",
		})

		self._txt_exclude_folder = self._ui.LineEdit({
			"ID": ID_TXT_EXCLUDE_FOLDER,
			"Events": {"TextEdited": True, "TextChanged": True},
		})

	def match_mediapool_folder_editor(self) -> object:
		"""Return the In Media Pool Folder `LineEdit`"""

		return self._txt_match_folder

	def exclude_mediapool_folder_editor(self) -> object:
		"""Return the In Media Pool Folder `LineEdit`"""

		return self._txt_exclude_folder

	def layout(self):
		return self._ui.VGroup([
			self._chk_refresh,
			
			self._ui.Label({"FrameStyle": 4}),

			self._ui.HGroup([
				self._chk_match_name,
				self._txt_match_name
			]),
			self._lbl_match_name_explained,

			self._ui.Label({"FrameStyle": 4}),

			self._ui.HGroup([
				self._chk_match_folder,
				self._lbl_match_folder_master,
				self._txt_match_folder,
			]),


			self._ui.HGroup([
				self._chk_exclude_folder,
				self._lbl_exclude_folder_master,
				self._txt_exclude_folder,
			]),

			self._ui.Label({"FrameStyle": 4}),

			self._ui.VGap(100),
		])