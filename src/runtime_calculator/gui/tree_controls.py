from .abstract_widget import TRTAbstractWidget

ID_BTN_ADD_LATEST   = "btn_add_latest"
ID_BTN_ADD_SELECTED = "btn_add_selected"
ID_BTN_CLEAR        = "btn_clear_list"

class TRTTreeControls(TRTAbstractWidget):
	"""Add/Clear Trim Items"""

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		self._btn_add_latest   = self._ui.Button({"Weight": 0, "Text": "Add Latest Reels", "ID": ID_BTN_ADD_LATEST})
		self._btn_add_selected = self._ui.Button({"Weight": 0, "Text": "Add Selected",     "ID": ID_BTN_ADD_SELECTED})
		self._btn_clear        = self._ui.Button({"Weight": 0, "Text": "Clear",            "ID": ID_BTN_CLEAR})

	def set_enabled(self, is_enabled:bool):

		self._btn_add_latest.Enabled = is_enabled
		self._btn_add_selected.Enabled = is_enabled
		self._btn_clear.Enabled = is_enabled

	def layout(self) -> object:

		return self._ui.HGroup([
			self._btn_add_latest,
			self._btn_add_selected,
			self._ui.HGap(),
			self._btn_clear
		])