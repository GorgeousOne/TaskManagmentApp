import bisect

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide2.QtCore import Qt, QTime

from uis.ui_note_entry import UINoteEntry


class UIDateSection(QWidget):
	def __init__(self, date):
		super().__init__()
		self.date = date

		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.date_label = QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd d. MMMM"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.date_label.setObjectName("date_label")
		self.verticalLayout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		self.line = QFrame(self)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		self.line.setObjectName("line")
		self.verticalLayout.addWidget(self.line)

		self.note_area = QWidget(self)
		self.note_area.setObjectName("note_area")

		self.verticalLayout.addWidget(self.note_area)

		self.verticalLayout_2 = QVBoxLayout(self.note_area)
		self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
		self.verticalLayout_2.setSpacing(10)
		self.verticalLayout_2.setObjectName("verticalLayout_2")

		self._times = []
		self._note_entries = []

	def is_empty(self):
		return len(self._note_entries) == 0

	def display_note(self, new_note):

		new_time = new_note.time if new_note.time else QTime(0, 0)
		index = bisect.bisect_right(self._times, new_time)
		new_entry = UINoteEntry(new_note, self)

		self._times.insert(index, new_time)
		self.note_area.layout().insertWidget(index, new_entry)
		self._note_entries.insert(index, new_entry)
		return new_entry

	def remove_note(self, note):
		for i in range(len(self._times)):
			entry = self._note_entries[i]
			if entry._note == note:
				# self.note_area.layout().removeWidget(entry)
				entry.hide()
				entry.deleteLater()

				self._note_entries.remove(entry)
				self._times.pop(i)
				return
