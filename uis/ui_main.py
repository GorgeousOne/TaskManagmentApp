from PySide2 import QtCore, QtUiTools, QtGui
from uis.ui_project_bar import UiProjectsBar
from uis.ui_timeline import UiTimeline


class UiMainWindow:
	"""Loads the main window with the ui elements for the top bar, projects bar and task timeline in it"""
	def __init__(self, main_handler):
		self.window = QtUiTools.QUiLoader().load("./uis/scripts/ui_main.ui")
		self.window.setWindowTitle("Task Management App")
		self.window.setWindowIcon(QtGui.QIcon("./res/icons/squiggle3.png"))

		self.window.toggle_menu_btn.setIcon(QtGui.QIcon("./res/icons/burger.png"))
		self.window.create_task_btn.setIcon(QtGui.QIcon("./res/icons/plus.png"))
		self.window.create_project_btn.setIcon(QtGui.QIcon("./res/icons/circled-plus.png"))
		self.window.create_project_btn.setIconSize(QtCore.QSize(50, 50))

		self.window.toggle_menu_btn.clicked.connect(lambda: self.toggle_menu(55, 300))

		self.window.timeline_area.hide()

		self.window.projects_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.window.projects_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.timeline = UiTimeline(self.window.timeline_area, main_handler)
		self.projects_bar = UiProjectsBar(self.window.projects_area)

	def toggle_menu(self, min_extend, max_extend):
		"""Creates smooth opening and closing animation for the projects bar"""
		width = self.window.sidebar_frame.width()
		width_extend = max_extend if width == min_extend else min_extend

		self.window.animation = QtCore.QPropertyAnimation(self.window.sidebar_frame, b"maximumWidth")
		self.window.animation.setDuration(500)
		self.window.animation.setStartValue(width)
		self.window.animation.setEndValue(width_extend)
		self.window.animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
		self.window.animation.start()
