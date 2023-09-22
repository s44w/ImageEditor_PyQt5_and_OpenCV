from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QSlider, QDialog, QRubberBand
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent #
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
class ModdedQLabel(QLabel):
	clicked = QtCore.pyqtSignal()
	def __init__(self, centralWidget):
		QLabel.__init__(self, centralWidget)
		#self.is_cropping = 0
		#self.is_putting_text = 0
		self.is_selecting_region = False
		self.selected_region = None

		self.x = 0
		self.y = 0
		self.center_coords = (0,0)
		#self.setAlignment(QtCore.Qt.AlignCenter)


	#def mousePressEvent(self, event: QMouseEvent):
	#	return (self.x, self.y)
	def mousePressEvent(self, event: QMouseEvent):
		self.x = event.x()
		self.y = event.y()
		#self.clicked.emit()

		if self.is_selecting_region:
			self.originQPoint = event.pos()
			self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
			self.currentQRubberBand.setGeometry(
				QtCore.QRect(self.originQPoint, QtCore.QSize()))

			self.currentQRubberBand.show()

		#print(self.x, self.y)
		QLabel.mousePressEvent(self, event)

	def mouseMoveEvent(self, event: QMouseEvent):
		self.x = event.x()
		self.y = event.y()
		#print(self.x, self.y)
		if self.is_selecting_region:
			self.currentQRubberBand.setGeometry(
				QtCore.QRect(self.originQPoint, event.pos())
				.normalized())

		QLabel.mouseMoveEvent(self, event)

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
		if self.is_selecting_region:
			self.center_coords = ((event.x() - self.originQPoint.x())//2,
								  (event.y() - self.originQPoint.y())//2 )

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