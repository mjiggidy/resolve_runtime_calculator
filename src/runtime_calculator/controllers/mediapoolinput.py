from resolvecommon.session import resolve
from ..utils import folders

class TRTMediaPoolInputController:

	def __init__(self, line_edit:object):

		self._line_edit        = line_edit
		self._last_edit_length = 0

	def register_window_handle(self, window_handle:object):
		"""Register `TextEdited` event with dispatcher window handle"""
		
		# TODO: Figure out how to set TextEdited event on the line edit in the constructor?

		window_handle.On[self._line_edit.ID].TextEdited = self._test_text_changed

	def _test_text_changed(self, event:dict):
		"""Test event for media pool browser thing"""

		user_text:str = event.get("Text","")



		root = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetRootFolder()

		path_normalized = user_text.lstrip("/")

		#print(event)

		if not user_text:
			self._last_edit_length = 0
			return
		
		if "/" in path_normalized:

			last_sep_index = path_normalized.rfind("/")

			try:
				current_folder = folders.get_folder_from_path(path_normalized[:last_sep_index+1], root)
			except:
				print("invalid source path", path_normalized[:last_sep_index+1])
				self._last_edit_length = len(user_text)
				return

			partial_folder = path_normalized[last_sep_index+1:]

		else:
			current_folder = root
			partial_folder = path_normalized

		subfolders = sorted(
			filter(lambda f: f.GetName().startswith(partial_folder), current_folder.GetSubFolderList()),
			key=lambda f:f.GetName()
		)

		#self._gui_window.set_subfolders_list([f.GetName() for f in subfolders])

		if len(user_text) <= self._last_edit_length:
			self._last_edit_length = len(user_text)
			return

		self._last_edit_length = len(user_text)

		if subfolders:

			next_subfolder_name = subfolders[0].GetName()

			autocomplete_text = next_subfolder_name[len(partial_folder):]

			full_replace_text = user_text + autocomplete_text

			self._line_edit.Text = full_replace_text

			self._line_edit.SetSelection(len(user_text), len(full_replace_text))