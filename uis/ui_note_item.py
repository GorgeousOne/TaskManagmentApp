import re
from PySide2 import QtWidgets, QtGui, QtUiTools
from PySide2.QtCore import Qt
import utils


def highlight_urls(text):
	"""A primitive method to turn some types of urls inside a string into hyperlinks"""
	hyper_words = []
	for word in text.split():
		if re.search("\.[com|net|org|io|de]", word):
			hyper_words.append("""<a href={url}>{url}</>""".format(url=word))
		else:
			hyper_words.append(word)
	return " ".join(hyper_words)


class UiNoteItem(QtWidgets.QFrame):
	def __init__(self, note, date_section):
		super().__init__()

		note.add_listener(self)
		self.note = note
		self.date_section = date_section
		self.setStyleSheet(
			"""
			border: 0px solid;
			border-radius: 5px;
			"""
		)

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.setMaximumWidth(1400)

		self.content = QtUiTools.QUiLoader().load("./uis/res/ui_note_item.ui")
		self.verticalLayout.addWidget(self.content)

		self.content.description_label.setOpenExternalLinks(True)

		self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self.date_section)
		self.shadow_effect.setBlurRadius(10)
		self.shadow_effect.setOffset(0)
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 40))
		self.setGraphicsEffect(self.shadow_effect)

		self.content.details_widget.hide()

		self.gray_out_effect = QtWidgets.QGraphicsColorizeEffect(self)
		self.gray_out_effect.setColor(Qt.white)
		self.gray_out_effect.setStrength(0.95)
		self.content.button_bar.setGraphicsEffect(self.gray_out_effect)

		self.update_data()

	def enterEvent(self, event):
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 60))
		self.gray_out_effect.setEnabled(False)

	def leaveEvent(self, event):
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 40))
		self.gray_out_effect.setEnabled(True)

	def mouseReleaseEvent(self, event):
		collapse = self.content.details_widget.isVisible()
		if collapse:
			self.collapse_details()
		else:
			self.fold_out_details()

	def fold_out_details(self):
		self.content.details_widget.setVisible(True)
		self.content.title_label.setStyleSheet("""font: 63 12pt "Segoe UI Semibold";""")

	def collapse_details(self):
		self.content.details_widget.setVisible(False)
		self.content.title_label.setStyleSheet("")

	def update_data(self):
		"""Updates the displayed information about the note."""
		self.content.title_label.setText(self.note.title)
		self.content.description_label.setText(highlight_urls(self.note.description))

		if self.note.time:
			self.content.time_label.show()
			self.content.time_label.setText(self.note.time.toString("HH:mm"))
		else:
			self.content.time_label.hide()

		if self.note.get_is_done():
			self.content.toggle_done_btn.setText("Undo")
			self.shadow_effect.setEnabled(False)
			styles = utils.replace_property(self.styleSheet(), "background", "rgb(240, 245, 255)")
			styles = utils.replace_property(styles, "color", "rgb(200, 200, 200)")
			self.setStyleSheet(styles)

		else:
			self.content.toggle_done_btn.setText("Complete")
			self.shadow_effect.setEnabled(True)
			styles = utils.replace_property(self.styleSheet(), "background", "rgb(255, 255, 255)")
			styles = utils.replace_property(styles, "color", "rgb(0, 0, 0)")
			self.setStyleSheet(styles)

	def __lt__(self, other):
		if not isinstance(other, UiNoteItem):
			return False
		return self.note < other.note
