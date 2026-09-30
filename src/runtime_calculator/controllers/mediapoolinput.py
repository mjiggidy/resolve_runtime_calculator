from resolvecommon.session import resolve
from ..utils import folders

class TRTMediaPoolInputController:

	def __init__(self, line_edit:object):

		self._line_edit        = line_edit

		self._color_warning    = {"R": 1, "G": 0, "B": 0, "A": 0.25}
		self._color_valid      = self._line_edit.BackgroundColor or {"R": 0, "G": 0, "B": 0, "A": 1}

		self._last_edit_length = 0

		self.validate_path()

	def register_window_handle(self, window_handle:object):
		"""Register `TextEdited` event with dispatcher window handle"""
		
		# TODO: Figure out how to enable these evenvts on the line edit in the constructor?

		window_handle.On[self._line_edit.ID].TextEdited      = self._on_user_changed_path
		window_handle.On[self._line_edit.ID].EditingFinished = self._on_user_path_settled

	def _on_user_path_settled(self, event:dict):
		"""Reformat/standardize user input"""

		self._line_edit.Text = self._line_edit.Text.strip("/")

		self.validate_path()

	def validate_path(self):

		try:
			
			folders.get_folder_from_path(
				self._line_edit.Text,
				resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetRootFolder()
			)

		except Exception as e:
			print(f"Exception for {self._line_edit.Text} was {e}")
			self._line_edit.BackgroundColor = self._color_warning
		
		else:
			self._line_edit.BackgroundColor = self._color_valid

	def _on_user_changed_path(self, event:dict):
		"""Validate and autocomplete path on user text edited"""
		
		# Get user input and format for processing

		user_input:str = event["Text"]

		if not user_input:
			
			self._last_edit_length = 0
			return

		path_normalized = user_input.lstrip("/")

		root_folder = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetRootFolder()
		
		if "/" in path_normalized:

			# Resolve the base folder and split off the final child folder/partial folder name

			last_sep_index = path_normalized.rfind("/")
			base_path      = path_normalized[:last_sep_index+1]

			try:
				current_folder = folders.get_folder_from_path(base_path, root_folder)
			
			except:
			
				print("invalid source path", base_path)
				self._last_edit_length = len(user_input)
				return

			partial_folder = path_normalized[last_sep_index+1:]

		else:
			
			current_folder = root_folder
			partial_folder = path_normalized

		subfolders = sorted(
			filter(lambda f: f.GetName().startswith(partial_folder), current_folder.GetSubFolderList()),
			key=lambda f:f.GetName()
		)

		#self._gui_window.set_subfolders_list([f.GetName() for f in subfolders])

		if len(user_input) <= self._last_edit_length:
			self._last_edit_length = len(user_input)
			return

		self._last_edit_length = len(user_input)

		if subfolders:

			next_subfolder_name = subfolders[0].GetName()

			autocomplete_text = next_subfolder_name[len(partial_folder):]

			full_replace_text = user_input + autocomplete_text

			self._line_edit.Text = full_replace_text

			self._line_edit.SetSelection(len(user_input), len(full_replace_text))