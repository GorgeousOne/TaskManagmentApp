import bisect
from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from uis.ui_note_item import UiNoteItem


class UiDateSection(QtWidgets.QWidget):
	"""A widget for displaying all note items of one day together with a date as header"""
	def __init__(self, date):
		super().__init__()
		self.date = date
		self.note_items = []
		self.visible_item_count = 0

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)

		# creates the header
		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd, d. MMMM yy"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.vertical_layout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		# creates the dividing line
		self.line = QtWidgets.QFrame(self)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.vertical_layout.addWidget(self.line)

		# creates the area for the tasks to be displayed
		self.note_area = QtWidgets.QWidget(self)
		self.vertical_layout.addWidget(self.note_area)

		self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.note_area)
		self.vertical_layout_2.setContentsMargins(10, 10, 10, 10)
		self.vertical_layout_2.setSpacing(10)

	def note_count(self):
		"""Returns the amount of notes listed in this section"""
		return len(self.note_items)

	def any_notes_are_visible(self):
		"""Returns if any of the notes inside this section are visible with the currently applied project filter"""
		for note in self.note_items:
			if note.isVisible():
				return True
		return False

	def display_note(self, new_note):
		new_item = UiNoteItem(new_note, self)
		index = bisect.bisect_right(self.note_items, new_item)

		self.note_area.layout().insertWidget(index, new_item)
		self.note_items.insert(index, new_item)
		self.visible_item_count += 1
		return new_item

	def set_item_visible(self, item, is_visible):
		"""Sets visibility of an item and hides the section itself if no items are visible in it"""
		if self.visible_item_count == 0 and is_visible:
			self.show()

		item.setVisible(is_visible)
		self.visible_item_count += 1 if is_visible else -1

		if self.visible_item_count == 0:
			self.hide()

	def update_item(self, note):
		"""Updates the time/alphabet related position of an item inside this section after being changed"""
		item = self.get_item(note)
		self.note_items.remove(item)
		new_index = bisect.bisect_right(self.note_items, item)
		self.note_area.layout().insertWidget(new_index, item)
		self.note_items.insert(new_index, item)

	def remove_note(self, note):
		item = self.get_item(note)
		item.hide()
		item.deleteLater()
		self.note_items.remove(item)
		note.remove_listener(item)
		return

	def get_item(self, note):
		"""Returns the task item from this section associated with the given task"""
		for item in self.note_items:
			if item.note == note:
				return item
		raise Exception(str(note) + " not listed in " + self.date.toString("d. MMMM yy"))

	def __lt__(self, other):
		if not isinstance(other, UiDateSection):
			return False
		return self.date < other.date
