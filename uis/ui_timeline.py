import bisect
from uis.ui_date_section import UiDateSection


class UiTimeline:
	"""Handles displaying of tasks in a linear timeline, split into sections for each day"""
	def __init__(self, container, main_handler):
		"""container: QWidget that will be used to display the tasks"""
		self.main_handler = main_handler
		self.container = container
		self.layout = container.layout()

		self.date_sections = []
		self.displayed_notes = dict()

		self.are_done_notes_visible = True
		self.filtered_project = None
		self.out_filtered_items = []

	def display_note(self, note):
		"""Displays a task in the timeline. Creates a new section if there was no section with the tasks date before"""
		date = note.get_date()
		section = None

		for existing_section in self.date_sections:
			if existing_section.date == note.get_date():
				section = existing_section
				break

		if not section:
			section = self.insert_section(date)

		self.displayed_notes[note] = section
		note.add_listener(self)

		item = section.display_note(note)
		item.content.toggle_done_btn.clicked.connect(lambda: self.main_handler.toggle_note_completion(note))
		item.content.delete_btn.clicked.connect(lambda: self.main_handler.delete_note(note))
		item.content.edit_btn.clicked.connect(lambda: self.main_handler.start_editing_note(note))

	def on_note_change(self, note):
		"""Reorders a task after it's date/time was potentially being changed"""
		section = self.displayed_notes[note]
		if section.date == note.get_date():
			section.update_item(note)
		else:
			self.remove_note(note)
			self.display_note(note)

	def set_done_notes_visible(self, state):
		"""Hides or displays all tasks that are completed"""
		self.are_done_notes_visible = state

		for section in self.date_sections:
			for item in section.note_items:
				if item.note.is_done and item not in self.out_filtered_items:
					section.set_item_visible(item, state)

	def filter_project(self, project):
		"""Hides all elements in the timeline that do not belong to the given project"""
		for item in self.out_filtered_items:
			if self.are_done_notes_visible or not item.note.get_is_done():
				self.displayed_notes[item.note].set_item_visible(item, True)

		self.out_filtered_items.clear()

		# reset the filtered project if a project item was clicked twice
		if project == self.filtered_project:
			self.filtered_project = None
		else:
			self.filtered_project = project
		if not self.filtered_project:
			return

		for section in self.date_sections:
			for item in section.note_items:
				if item.note.get_project() != project:
					section.set_item_visible(item, False)
					self.out_filtered_items.append(item)

	def remove_note(self, note):
		note.remove_listener(self)
		section = self.displayed_notes[note]
		section.remove_note(note)

		if section.note_count() == 0:
			self.remove_section(section)
		del self.displayed_notes[note]

	def insert_section(self, new_date):
		"""Inserts a section for a new date"""
		new_section = UiDateSection(new_date)
		index = bisect.bisect(self.date_sections, new_section)

		self.date_sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section

	def remove_section(self, section):
		section.hide()
		section.deleteLater()
		self.date_sections.remove(section)
