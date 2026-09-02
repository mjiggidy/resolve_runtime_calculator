from .abstract_widget import TRTAbstractWidget

ID_TREE_VIEW = "tree_trims"

class TRTTreeResults(TRTAbstractWidget):

	def __init__(self, ui_manager:object):

		super().__init__(ui_manager)

		self._tree = self._ui.Tree({
			"ID": ID_TREE_VIEW,
			"Weight": 200,
			"AlternatingRowColors":True,
#			"SortingEnabled":True,
			"SelectionMode": "ExtendedSelection",
			"ItemsExpandable": False,
			"ColumnCount": 5,
			"RootIsDecorated": False,
			"UniformRowHeights": True,
			"Indentation": False,
			"Events": {"ItemActivated":True, "ItemDoubleClicked":True},
		})

		self._tree.SetHeaderLabels([
			"Name",
			"Runtime",
			"LFOA",
			"Head",
			"Tail",
		])

	def tree(self) -> object:

		return self._tree

	def selected_rows(self) -> list[tuple[int, object]]:
		"""Return a tuple of selected (index, TreeItem)s"""

		return [(self._tree.IndexOfTopLevelItem(itm), itm) for itm in self._tree.SelectedItems().values()]

	def item_index(self, tree_item:object) -> int:
		"""Return the index of a tree item"""

		idx = self._tree.IndexOfTopLevelItem(tree_item)

		if idx is not None:
			return idx

		raise IndexError(f"Item {idx} not found in tree view")

	def layout(self) -> object:

		return self._tree

	def add_text_row(self, text_per_column:list[str]):

		item = self._tree.NewItem()

		for idx, text in enumerate(text_per_column):
			item.Text[idx] = text

		item.TextAlignment[1] = 130 # QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter  AHAHAHA I'M SMART
		item.TextAlignment[2] = 130
		item.TextAlignment[3] = 130
		item.TextAlignment[4] = 130

		self._tree.AddTopLevelItem(item)

#		print(dir(item.GetData))

	def clear(self):

		self._tree.Clear()