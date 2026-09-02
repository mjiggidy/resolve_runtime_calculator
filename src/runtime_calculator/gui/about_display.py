from .abstract_widget import TRTAbstractWidget

class TRTAboutDisplay(TRTAbstractWidget):
	"""About!"""

	def __init__(self, ui_manager:object, app_version:str, url_github:str, url_donate:str):

		super().__init__(ui_manager)

		font_about = self._ui.Font({"PointSize": 10})

		self._lbl_about_author = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": "Written by Michael Jordan"
		})

		self._lbl_about_links  = self._ui.Label({
			"Weight":0,
			"Font": font_about,
			"Text": f"v{app_version} | <a href=\"{url_github}\">Github</a> | <a href=\"{url_donate}\">Donate</a>",
			"OpenExternalLinks": True,
		})

		#self._lbl_about_links.SetOpenExternalLinks(True)

	def layout(self) -> object:
		
		return self._ui.HGroup([
			self._lbl_about_author,
			self._ui.HGap(),
			self._lbl_about_links,
		])