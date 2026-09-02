import abc

class TRTAbstractWidget(abc.ABC):
	"""An abstract TRT widget"""

	def __init__(self, ui_manager:object):
		
		self._ui = ui_manager

	@abc.abstractmethod
	def layout(self) -> object:
		"""Return a `UIManager` widget"""