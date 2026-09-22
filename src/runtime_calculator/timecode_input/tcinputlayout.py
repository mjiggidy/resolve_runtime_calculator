import uuid

class TRTTimecodeInputLayout:

	def __init__(self, ui_manager:object, /, timecode_text:str|None=None):

		self._ui = ui_manager

		self._txt_timecode = self._ui.LineEdit({
			"ID": str(uuid.uuid1()),
			"Weight": 100,
			"Text": timecode_text or "",
			"PlaceholderText": "0:00",
			"Events": {"EditingFinished": True},
		})

		timecode_alignment = self._txt_timecode.GetAlignment()
		timecode_alignment["AlignLeft"] = False
		timecode_alignment["AlignRight"] = True
		self._txt_timecode.SetAlignment(timecode_alignment)

	def layout(self) -> object:

		return self._txt_timecode

	def id(self) -> str:

		return self._txt_timecode.ID

	def set_weight(self, weight:int=1):

		self._txt_timecode.Weight = weight

	def set_enabled(self, is_enabled:bool):

		self._txt_timecode.Enabled = is_enabled

	def text(self) -> str:

		return self._txt_timecode.Text

	def set_text(self, text:str):

		self._txt_timecode.Text = text

	def set_minimum_size(self, minimum_size:list[int]):

		self._txt_timecode.MinimumSize = minimum_size