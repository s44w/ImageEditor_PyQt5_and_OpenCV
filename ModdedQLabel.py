from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QSlider, QDialog
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5 import QtCore
from PyQt5 import QtWidgets
class ModdedQLabel(QLabel):
	clicked = QtCore.pyqtSignal()
	def __init__(self, centralWidget):
		QLabel.__init__(self, centralWidget)
		#self.is_cropping = 0
		#self.is_putting_text = 0
		self.x = 0
		self.y = 0

		#self.setAlignment(QtCore.Qt.AlignCenter)


	#def mousePressEvent(self, event: QMouseEvent):
	#	return (self.x, self.y)
	def mousePressEvent(self, ev: QMouseEvent):
		self.clicked.emit()
		QLabel.mousePressEvent(self, ev)

	def mouseMoveEvent(self, event: QMouseEvent):
		self.x = event.x()
		self.y = event.y()
		print(self.x, self.y)
		QLabel.mouseMoveEvent(self, event)

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y