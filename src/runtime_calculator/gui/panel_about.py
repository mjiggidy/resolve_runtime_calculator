from .abstract_widget import TRTAbstractWidget

class TRTAboutPane(TRTAbstractWidget):
	"""About!"""

	def __init__(self, ui_manager:object, app_version:str, url_github:str, url_donate:str|None):

		super().__init__(ui_manager)

		# Set up all the little things
		# Probably want to add individual setters leter
		# BUT NOT NEEDED SO I DUNNO I MEAN THIS WORKS FINE FOR ME

		elements = [
			f"v{app_version}",
			f"<a href=\"{url_github}\">Github</a>",
		 ]
		if url_donate is not None:
			elements.append(f"<a href=\"{url_donate}\">Donate</a>")

		font_about = self._ui.Font({"PointSize": 10})

		self._lbl_about_author = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": "Written by Michael Jordan"
		})

		self._lbl_about_links  = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": str(" | ").join(elements),
			"OpenExternalLinks": True,
		})

		#self._lbl_about_links.SetOpenExternalLinks(True)

	def layout(self) -> object:
		
		return self._ui.HGroup([
			self._lbl_about_author,
			self._ui.HGap(),
			self._lbl_about_links,
		])