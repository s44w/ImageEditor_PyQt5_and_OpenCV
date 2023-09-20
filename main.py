from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFrame, QLabel, QFileDialog, QSlider, QDialog
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from qcrop.ui import QCrop
from PyQt5.QtCore import Qt, QRect
import sys
import numpy as np
import cv2

import BackUpClass
import opencv_basic_functions as cvf
import BackUpClass as BackUp
import ModdedQLabel as ModdedQLabel

#TODO:
# Necessary: Done: UnDo, ReDo buttons, stack/array with backups
# 			 Undone: crop, paint functions, text, blur brush
# Additionally: Crop function only by PyQt or OpenCV, Fix Rotate function
# https://www.life2coding.com/crop-image-using-mouse-click-movement-python/
#

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("image.ui", self)

		self.pixmap = QPixmap()
		self.image_path = None
		self.cv2image = None
		self.cv2image_used = False
		self.is_highlighting_area = 0
		self.rect_coords = []
		self.backup = BackUpClass.BackupFiles()

		# Define our widgets
		self.buttonFlipHoriz = self.findChild(QPushButton, "buttonFlipHoriz")
		self.buttonFlipVertic = self.findChild(QPushButton, "buttonFlipVertic")
		self.buttonOpenFile = self.findChild(QPushButton, "buttonOpenFile")
		self.buttonSaveFile = self.findChild(QPushButton, "buttonSaveFile")
		self.buttonCrop = self.findChild(QPushButton, "buttonCrop")
		self.buttonUnDo = self.findChild(QPushButton, "buttonUnDo")
		self.buttonReDo = self.findChild(QPushButton, "buttonReDo")
		self.buttonText = self.findChild(QPushButton, "buttonText")
		#self.buttonRotate = self.findChild(QPushButton, "buttonRotate")

		#self.firstLabel = self.findChild(QLabel, "labelPhoto")

		self.labelPhoto = ModdedQLabel.ModdedQLabel(self)
		self.labelPhoto.setGeometry(QRect(180, 100, 700, 600))
		self.labelPhoto.setFrameShape(QFrame.Box)
		self.labelPhoto.setText("")

		self.horizontalSliderRotation = self.findChild(QSlider, "horizontalSliderRotation")
		self.horizontalSliderHue = self.findChild(QSlider, "horizontalSliderHue")
		self.horizontalSliderSight = self.findChild(QSlider, "horizontalSliderSight")
		self.horizontalSliderValue = self.findChild(QSlider, "horizontalSliderValue")

		# Click The Buttons
		self.buttonOpenFile.clicked.connect(self.open_image)
		self.buttonSaveFile.clicked.connect(self.save_image)
		self.buttonFlipHoriz.clicked.connect(lambda: self.flip_image(0))
		self.buttonFlipVertic.clicked.connect(lambda: self.flip_image(1))
		self.buttonCrop.clicked.connect(self.crop_image)
		self.buttonUnDo.clicked.connect(self.act_undo)
		self.buttonReDo.clicked.connect(self.act_redo)
		self.buttonText.clicked.connect(self.add_text)

		# Click The Label
		self.labelPhoto.clicked.connect(lambda: self.rectangle_coordinates(self.rect_coords))

		# Move The Sliders
		self.horizontalSliderRotation.sliderReleased.connect(self.rotate_image)
		self.horizontalSliderHue.sliderReleased.connect(self.change_hue)
		self.horizontalSliderSight.sliderReleased.connect(self.change_sight)
		self.horizontalSliderValue.sliderReleased.connect(self.change_value)

		# Show The App
		self.show()

	def reset_settings(self):
		self.backup.clear_elems()
		self.cv2image = None
		self.cv2image_used = False
		self.horizontalSliderRotation.setValue(0)

	def set_fixed_pixmap(self):
		self.labelPhoto.setPixmap(self.pixmap.scaled
								  (self.labelPhoto.width(), self.labelPhoto.height(),
								   Qt.KeepAspectRatio, Qt.SmoothTransformation))

	def open_image(self):
		import os
		os.chdir('D:/PhotoEditor')
		self.image_path, _ = QFileDialog.getOpenFileName(self, "Open File",
														 None, "All Files (*.png *.jpg *.jpeg);;PNG Files (*.png);;Jpg Files (*.jpg);;Jpeg Files(*.jpeg)")
		# Open The Image

		if self.image_path:
			self.reset_settings()

			#label_size = self.labelPhoto.height(), self.labelPhoto.width()
			self.pixmap = QPixmap(self.image_path)
			self.check_n_set_cv2image()
			self.backup.add_elem(self.cv2image)
			# Add Pic to label
			#image_size = self.pixmap.height(), self.pixmap.width()
			
			self.set_fixed_pixmap()

	def save_image(self):
		save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", None, "All Files (*.png *.jpg *.jpeg)")
		if save_path:
			self.pixmap.save(save_path, "PNG", 100)


	def convert_cv_to_pixmap(self, cvImage):
		if self.cv2image_used:
			height, width, channel = self.cv2image.shape
			bytesPerLine = 3*width
			qImage = QImage(cvImage.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
			self.cv2image = cvImage

			#self.backup.add_elem(self.cv2image)
			return QPixmap(qImage)

	def convert_pixmap_to_mat(self, qImage: QImage):
		new_image = qImage.convertToFormat(QImage.Format_RGB888)
		width = new_image.width()
		height = new_image.height()
		bits = new_image.bits()

		mat = cv2.Mat(height, width, cv2.CV_8UC3, bits, new_image.bytesPerLine())
		return mat

	def check_n_set_cv2image(self):
		if not self.cv2image_used:
			self.cv2image = cv2.imread(self.image_path)
			self.cv2image_used = True

	def flip_image(self, mode): #0 to horizontally, 1 to vertically
		if self.image_path:
			self.check_n_set_cv2image()

			new_image = cvf.flip_image(self.cv2image, mode)
			self.pixmap = self.convert_cv_to_pixmap(new_image)
			self.set_fixed_pixmap()

	def rotate_image(self):
		if self.image_path:
			self.check_n_set_cv2image()

			degrees = self.horizontalSliderRotation.value()

			new_image = cvf.rotate_image(self.cv2image, degrees)
			self.pixmap = self.convert_cv_to_pixmap(new_image)
			self.backup.add_elem(self.cv2image)
			self.set_fixed_pixmap()

	def crop_image(self):
		crop_tool = QCrop(self.pixmap)
		status = crop_tool.exec()


		if status == QDialog.Accepted:
			qImage = QImage(crop_tool.image)
			self.pixmap = QPixmap.fromImage(qImage)
			self.cv2image = self.convert_pixmap_to_mat(qImage)


		self.set_fixed_pixmap()

	def change_hue(self):
		self.check_n_set_cv2image()

		imageHSV = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2HSV)
		imageHSV[:,:,0] = self.horizontalSliderHue.value()  #[h,s,v]

		self.cv2image = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)
		self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
		self.backup.add_elem(self.cv2image)
		self.set_fixed_pixmap()

	def change_sight(self):
		self.check_n_set_cv2image()

		imageHSV = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2HSV)
		imageHSV[:,:,1] = self.horizontalSliderSight.value()

		self.cv2image = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)
		self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
		self.backup.add_elem(self.cv2image)
		self.set_fixed_pixmap()

	def change_value(self):
		self.check_n_set_cv2image()

		imageHSV = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2HSV)
		imageHSV[:,:,2] = self.horizontalSliderValue.value()

		self.cv2image = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)
		self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
		self.backup.add_elem(self.cv2image)
		self.set_fixed_pixmap()

	def act_undo(self):
		if self.image_path:
			self.check_n_set_cv2image()
			self.backup.event_undo()
			self.cv2image = self.backup.get_cur_version()
			self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
			self.set_fixed_pixmap()


	def act_redo(self):
		if self.image_path:
			self.check_n_set_cv2image()
			self.backup.event_redo()
			self.cv2image = self.backup.get_cur_version()
			self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
			self.set_fixed_pixmap()


	def rectangle_coordinates(self, coordinates):
		if self.is_highlighting_area:

			x, y = self.labelPhoto.get_x(), self.labelPhoto.get_y()
			coordinates.append(x)
			coordinates.append(y)

			if len(self.rect_coords)==4:
				#self.rect_coords.clear()
				self.add_text()
				#self.is_highlighting_area = False

	def add_text(self):
		if self.image_path:
			self.is_highlighting_area^=1

			if len(self.rect_coords) == 4:
				#self.
				print(self.rect_coords)
				self.rect_coords.clear()
			'''
			if self.labelPhoto.clicked:
				x1,y1,x2,y2 = self.rectangle_coordinates()
				print(x1,y1,x2,y2)
			'''












# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
