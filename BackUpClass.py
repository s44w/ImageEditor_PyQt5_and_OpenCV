import numpy as np
class BackupFiles:
	def __init__(self):
		self.last_versions = []
		self.current_version = np.empty([0])
		self.future_versions = []

	def get_cur_version(self):
		return self.current_version

	def get_prev_version(self):
		if len(self.last_versions):
			return self.last_versions[-1]
		else:
			return self.current_version

	def add_elem(self, elem):
		if self.current_version.size: #!=None
			self.last_versions.append(self.current_version)

		if len(self.last_versions)>10:
			self.last_versions.pop(0)

		self.current_version = elem


	def event_undo(self):
		if len(self.last_versions) > 0:
			tmp_ver = self.last_versions.pop()

			self.future_versions.append(self.current_version)
			if len(self.future_versions)>10:
				self.future_versions.pop(0)

			self.current_version = tmp_ver

	def event_redo(self):
		if len(self.future_versions)>0:
			tmp_ver = self.future_versions.pop()

			self.last_versions.append(self.current_version)
			if len(self.last_versions)>10:
				self.last_versions.pop(0)

			self.current_version = tmp_ver

	def clear_elems(self):
		if self.last_versions:
			self.last_versions.clear()
		if self.future_versions:
			self.future_versions.clear()
