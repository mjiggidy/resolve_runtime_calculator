from .abstract_widget import TRTAbstractWidget

ID_WINDOW_SETTINGS    = "win_settings"
ID_CHECK_REFRESH      = "chk_refresh"
ID_CHECK_MATCH_NAME   = "chk_match_name"
ID_TXT_MATCH_NAME     = "txt_match_name"
ID_CHK_MATCH_FOLDER   = "chk_match_folder"
ID_TXT_MATCH_FOLDER   = "txt_match_folder"
ID_CHK_EXCLUDE_FOLDER = "chk_exclude_folder"
ID_TXT_EXCLUDE_FOLDER = "txt_exclude_folder"

ID_BTN_SAVE = "btn_settings_save"

TXT_TIP_FONT_POINT_SIZE = 10

class TRTSettingsWindow(TRTAbstractWidget):

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		# Refresh project

		self._chk_refresh = self._ui.CheckBox({
			"ID": ID_CHECK_REFRESH,
			"Weight": 0,
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
			"Weight": 0,
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

		self._btn_save = self._ui.Button({
			"ID": ID_BTN_SAVE,
			"Weight": 0,
			"Text": "Save",
		})

		# FFOA Marker Name

		self._lbl_ffoa_name = self._ui.Label({
			"Weight": 0,
			"Text": "FFOA Marker Name Contains:"
		})

		self._txt_ffoa_name = self._ui.LineEdit({
			"PlaceholderText": "FFOA"
		})

		self._lbl_lfoa_name = self._ui.Label({
			"Weight": 0,
			"Text": "LFOA Marker Name Contains:"
		})

		self._txt_lfoa_name = self._ui.LineEdit({
			"PlaceholderText": "LFOA"
		})

	def match_mediapool_name_editor(self) -> object:
		"""Return the name pattern LineEdit"""

		return self._txt_match_name

	def match_mediapool_name_enabler(self) -> object:
		"""Return the name pattern `CheckBox`"""

		return self._chk_match_name
	
	def match_mediapool_folder_editor(self) -> object:
		"""Return the In Media Pool Folder `LineEdit`"""

		return self._txt_match_folder

	def match_mediapool_folder_enabler(self) -> object:
		"""Return the In Media Pool Folder `CheckBox`"""

		return self._chk_match_folder

	def exclude_mediapool_folder_editor(self) -> object:
		"""Return the In Media Pool Folder `LineEdit`"""

		return self._txt_exclude_folder

	def exclude_mediapool_folder_enabler(self) -> object:
		"""Return the In Media Pool Folder `CheckBox`"""

		return self._chk_exclude_folder

	def chk_refresh_project(self) -> object:
		"""Return the Refresh check"""

		return self._chk_refresh

	def ffoa_marker_editor(self) -> object:
		"""Return the `LineEdit` for the FFOA marker name"""

		return self._txt_ffoa_name

	def lfoa_marker_editor(self) -> object:
		"""Return the `LineEdit` for the LFOA marker name"""

		return self._txt_lfoa_name

	def layout(self):
		return self._ui.VGroup([

			self._chk_refresh,
			
			self._ui.Label({
				"Weight": 0,
				"FrameStyle": 4
			}),

			self._ui.HGroup({
				"Weight":0,
			},[
				self._chk_match_name,
				self._txt_match_name
			]),
			self._lbl_match_name_explained,

			self._ui.Label({
				"Weight": 0,
				"FrameStyle": 4
			}),


			self._ui.HGroup({
				"Weight":0,
			},[
				self._chk_match_folder,
				self._lbl_match_folder_master,
				self._txt_match_folder,
			]),


			self._ui.HGroup({
				"Weight": 0,
			},[
				self._chk_exclude_folder,
				self._lbl_exclude_folder_master,
				self._txt_exclude_folder,
			]),

			self._ui.Label({
				"Weight": 0,
				"FrameStyle": 4
			}),


			self._ui.HGroup({
				"Weight": 0,
			},[
				self._ui.VGroup({
					"Weight": 0,
				},[
					self._lbl_ffoa_name,
					self._txt_ffoa_name
				]),
				self._ui.HGap(),
				self._ui.VGroup({
					"Weight": 0,
				},[
					self._lbl_lfoa_name,
					self._txt_lfoa_name
				]),
			]),

			self._ui.Label({
				"Weight": 0,
				"FrameStyle": 4
			}),

			self._ui.VGap(),

			self._ui.HGroup({
				"Weight": 0,
			},[
				self._ui.HGap(),
				self._btn_save,
			]),
		])