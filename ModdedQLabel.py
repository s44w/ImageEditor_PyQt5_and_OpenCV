from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QSlider, QDialog, QRubberBand
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent, QPainter, QColor, QPaintEvent
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
class ModdedQLabel(QLabel):
	clicked = QtCore.pyqtSignal()
	def __init__(self, centralWidget):
		QLabel.__init__(self, centralWidget)
		self.is_cropping = False
		self.is_putting_text = False
		self.selected_region = None

		self.x = 0
		self.y = 0
		#self.height = 0
		#self.width = 0
	'''
	def paintEvent(self, event):
		super(ModdedQLabel, self).paintEvent(event)
		self.painter = QPainter(self)
		pos = QtCore.QPoint(self.x, self.y)
		self.painter.begin(self)
		self.painter.drawText(pos, 'hello')
		self.painter.setPen(QColor(255, 255, 255))
		self.painter.end()
	'''
	def mousePressEvent(self, event: QMouseEvent):
		self.x = event.x()
		self.y = event.y()

		if self.is_cropping:
			self.originQPoint = event.pos()
			self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
			self.currentQRubberBand.setGeometry(
				QtCore.QRect(self.originQPoint, QtCore.QSize()))
			self.currentQRubberBand.show()

		QLabel.mousePressEvent(self, event)

	def mouseMoveEvent(self, event: QMouseEvent):
		self.x = event.x()
		self.y = event.y()
		#print(self.x, self.y)
		if self.is_cropping or self.is_putting_text:
			self.currentQRubberBand.setGeometry(
				QtCore.QRect(self.originQPoint, event.pos())
				.normalized())

		QLabel.mouseMoveEvent(self, event)

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
		self.x = event.x()
		self.y = event.y()

		if self.is_cropping:
			self.currentQRubberBand.hide()
			curQRect = self.currentQRubberBand.geometry()
			self.currentQRubberBand.deleteLater()
			self.selected_region = self.pixmap().copy(curQRect)

		self.clicked.emit()



	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_selected_region(self):
		return self.selected_region

	def get_cropping_bool(self):
		return self.is_cropping
	def get_puttingText_bool(self):
		return self.is_putting_text

	def set_cropping_bool(self, crop: bool):
		self.is_cropping = crop

	def set_puttingText_bool(self, text: bool):
		self.is_putting_text = text