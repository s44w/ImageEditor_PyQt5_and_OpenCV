from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFrame, QLabel, QStackedWidget,\
	QFileDialog, QSlider, QDialog,  QColorDialog, QLineEdit
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent, QPainter, QColor
from qcrop.ui import QCrop
from PyQt5.QtCore import Qt, QRect, QPoint
import sys
import numpy as np
import cv2

import BackUpClass
import opencv_basic_functions as cvf
import BackUpClass as BackUp
import ModdedQLabel
import TextEditClass
#TODO:
# Necessary: Done: UnDo, ReDo buttons, stack/array with backups
# 			 Undone: crop, paint functions, text, blur brush, return slider values when Undo
# Additionally: Crop function only by PyQt or OpenCV, Fix Rotate function
# https://www.life2coding.com/crop-image-using-mouse-click-movement-python/
#

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("image.ui", self)

		self.pixmap = QPixmap()
		self.painter = QPainter()
		self.image_path = None
		self.cv2image = None
		self.cv2image_used = False
		self.is_highlighting_area = 0
		self.is_cropping = False
		self.is_adding_text = False

		self.tmpRegion = None
		self.backup = BackUpClass.BackupFiles()
		self.textClass = TextEditClass.TextEdit()


		# Define our widgets
		self.buttonFlipHoriz = self.findChild(QPushButton, "buttonFlipHoriz")
		self.buttonFlipVertic = self.findChild(QPushButton, "buttonFlipVertic")
		self.buttonOpenFile = self.findChild(QPushButton, "buttonOpenFile")
		self.buttonSaveFile = self.findChild(QPushButton, "buttonSaveFile")
		self.buttonCrop = self.findChild(QPushButton, "buttonCrop")
		self.buttonUnDo = self.findChild(QPushButton, "buttonUnDo")
		self.buttonReDo = self.findChild(QPushButton, "buttonReDo")
		self.buttonText = self.findChild(QPushButton, "buttonText")
		self.buttonColor = self.findChild(QPushButton, "buttonColor")

		#self.buttonRotate = self.findChild(QPushButton, "buttonRotate")

		#self.firstLabel = self.findChild(QLabel, "labelPhoto")
		self.buttonChooseColor = self.findChild(QPushButton, "buttonChooseColor")
		self.lineEditText = self.findChild(QLineEdit, "lineEditText")

		self.labelPhoto = ModdedQLabel.ModdedQLabel(self)
		self.labelPhoto.setGeometry(QRect(180, 100, 700, 600))
		self.labelPhoto.setFrameShape(QFrame.Box)
		self.buttonChooseColor.clicked.connect(self.choose_text_color)

		#self.tmpLabel = ModdedQLabel.ModdedQLabel(self)
		self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
		self.stackedWidget.setCurrentIndex(0)


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
		self.buttonColor.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

		# Click The Label
		self.labelPhoto.clicked.connect(self.rectangle_coordinates)

		# Move The Sliders
		self.horizontalSliderRotation.sliderReleased.connect(self.rotate_image)
		self.horizontalSliderHue.sliderReleased.connect(self.change_hue)
		self.horizontalSliderSight.sliderReleased.connect(self.change_sight)
		self.horizontalSliderValue.sliderReleased.connect(self.change_value)

		self.lineEditText.textChanged.connect(self.input_text)
		# Show The App
		self.show()

	def reset_settings(self):
		self.backup.clear_elems()
		self.cv2image = None
		self.cv2image_used = False
		self.horizontalSliderRotation.setValue(0)

	def set_fixed_pixmap(self):
		self.labelPhoto.setPixmap(
			self.pixmap.scaled
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
		qImage = QImage(qImage.toImage().convertToFormat(QImage.Format_RGBX8888))
		#qImage = qImage.convertToFormat(QImage.Format_RGBX8888)
		ptr = qImage.bits()
		ptr.setsize(qImage.byteCount())
		cv_im_in = np.array(ptr, copy=True).reshape(qImage.height(), qImage.width(), 4)
		cv_im_in = cv2.cvtColor(cv_im_in, cv2.COLOR_BGRA2RGB)
		return cv_im_in

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



	def rectangle_coordinates(self):
			if self.labelPhoto.selected_region:
				self.tmpRegion = self.labelPhoto.get_selected_region()

				if self.labelPhoto.get_cropping_bool():  #crop
					self.pixmap = self.tmpRegion
					self.cv2image = self.convert_pixmap_to_mat(self.pixmap)
					self.cv2image_used = True





				#self.labelPhoto.set_puttingText_bool(False)
				#self.labelPhoto.set_cropping_bool(False)
				self.backup.add_elem(self.cv2image)
				self.set_fixed_pixmap()


	def add_text(self):
		if self.image_path:
			self.stackedWidget.setCurrentIndex(2) #choose panel with text settings
			self.labelPhoto.is_putting_text = True

			tmpCVimage = self.convert_pixmap_to_mat(self.pixmap)

			coords = self.labelPhoto.get_y(), self.labelPhoto.get_x()
			self.cv2image = cvf.put_text(tmpCVimage,
										 textLine=self.textClass.getText(),
										 coords=coords,
										 textSize=self.textClass.getTextSize(),
										 color=self.textClass.getTextColor())
			self.cv2image_used = True

			self.pixmap = self.convert_cv_to_pixmap(self.cv2image)

			self.backup.add_elem(self.cv2image)
			self.set_fixed_pixmap()



	def crop_image(self):
			if self.image_path:
				# qImage = self.tmpRegion
				self.is_highlighting_area ^= 1
				self.labelPhoto.is_selecting_region = True
				self.is_cropping = True
				# if self.tmpRegion:
					#	self.pixmap = self.tmpRegion
					# self.cv2image = self.convert_pixmap_to_mat(self.pixmap)

				#self.set_fixed_pixmap()

	def input_text(self):
		self.textClass.setText(self.lineEditText.text())
		#print(self.text.getText())





	def choose_text_color(self):
		dialog = QColorDialog(self)
		#dialog.exec_()
		color = dialog.getColor()
		self.buttonChooseColor.setStyleSheet("QWidget { background-color: %s }" %color.name())
		self.textClass.setTextColor(color.name())
		#print(color.name())













# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
