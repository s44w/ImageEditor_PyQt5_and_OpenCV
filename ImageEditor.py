from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QFileDialog, QColorDialog
from PyQt5 import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRect
from pathlib import Path
import sys
import numpy as np
import cv2

import BackUpClass
import opencv_basic_functions as cvf
import ModdedQLabel
import TextEditClass
from ui import Ui_MainWindow


class UI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUi(self)

        self.pixmap = QPixmap()
        self.painter = QPainter()
        self.image_path = None
        self.cv2image = None
        self.cv2image_used = False

        self.tmpRegion = None
        self.backup_cvimage = BackUpClass.BackupFiles()
        self.backup_scrolls_list = BackUpClass.BackupFiles()
        self.textClass = TextEditClass.TextEdit()

        self.labelBackground = ModdedQLabel.ModdedQLabel(self)
        self.setup_label_background()

        self.labelPhoto = ModdedQLabel.ModdedQLabel(self)
        self.labelPhoto.hide()

        self.stackedWidget.setCurrentIndex(0)
        # Click The Buttons
        self.buttonOpenFile.clicked.connect(self.open_image)
        self.buttonSaveFile.clicked.connect(self.save_image)
        self.buttonFlipHoriz.clicked.connect(lambda: self.flip_image(0))
        self.buttonFlipVertic.clicked.connect(lambda: self.flip_image(1))
        self.buttonCrop.clicked.connect(self.crop_image)
        self.buttonUnDo.clicked.connect(self.event_undo)
        self.buttonReDo.clicked.connect(self.event_redo)
        self.buttonText.clicked.connect(self.add_text_button_clicked)
        self.buttonColor.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.buttonChooseColor.clicked.connect(self.choose_text_color)
        self.buttonRotationMenu.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(3))
        self.buttonRotate90.clicked.connect(
            lambda: self.rotate_image(rotated=True))

        # Click The Label
        self.labelPhoto.clicked.connect(self.image_clicked_event)
        self.labelBackground.clicked.connect(self.open_image)

        # Move The Sliders
        self.horizontalSliderRotation.sliderReleased.connect(self.rotate_image)
        self.horizontalSliderHue.sliderReleased.connect(self.change_hue)
        self.horizontalSliderContrast.sliderReleased.connect(
            self.change_contrast)
        self.horizontalSliderBrightness.sliderReleased.connect(
            self.change_brightness)

        self.comboBoxFilters.currentIndexChanged.connect(
            self.choose_color_filter)

        self.lineEditText.textChanged.connect(self.input_text_event)
        self.comboTextSize.currentIndexChanged.connect(self.change_text_size)
        # Show The App
        self.show()

    #     # -------------------------SET FUNCTIONS----------------------------

    def reset_settings(self):
        self.backup_cvimage.clear_elems()
        self.cv2image = None
        self.cv2image_used = False
        self.horizontalSliderRotation.setValue(0)
        self.backup_scrolls_list.clear_elems()

    def check_cvimage(self):
        if not self.cv2image_used:
            self.cv2image = cv2.imread(self.image_path)
            self.cv2image_used = True

    def set_fixed_pixmap(self):
        self.labelPhoto.setPixmap(
            self.pixmap.scaled
            (self.labelBackground.size(),
             Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def setup_label_background(self):
        self.labelBackground.setGeometry(QRect(340, 30, 910, 650))
        self.labelBackground.setFrameShape(QFrame.Box)
        self.labelBackground.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('icons/add_image.png')
        self.labelBackground.setPixmap(pixmap)

    def setup_modded_label(self):
        cvheight = self.cv2image.shape[0]
        cvwidth = self.cv2image.shape[1]
        coef = min(self.labelBackground.height() / cvheight,
                   self.labelBackground.width() / cvwidth)

        newHeight = int(cvheight * coef)
        newWidth = int(cvwidth * coef)
        self.labelBackground.hide()

        self.labelPhoto.setGeometry(QRect(340, 30, newWidth, newHeight))
        self.labelPhoto.setFrameShape(QFrame.Box)
        self.labelPhoto.show()

    def setup_HSV_scrolls(self, h=0, s=0, v=0):
        self.horizontalSliderHue.setValue(h)
        self.horizontalSliderContrast.setValue(s)
        self.horizontalSliderBrightness.setValue(v)

    # -------------------------OPEN/SAVE FILE FUNCTIONS-----------------------

    def open_image(self):
        import os
        os.chdir('D:/PhotoEditor')
        self.image_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", None, "All Files (*.png *.jpg *.jpeg);;"
            "PNG Files (*.png);;Jpg Files (*.jpg)"
            ";;Jpeg Files(*.jpeg)")
        if self.image_path:
            self.reset_settings()

            self.pixmap = QPixmap(self.image_path)
            self.check_cvimage()

            self.setup_modded_label()
            self.set_fixed_pixmap()

            self.backup_cvimage.add_elem(self.cv2image)
            self.backup_scrolls_list.add_elem(np.array([0, 0, 0]))

    def save_image(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", None, "All Files (*.png *.jpg *.jpeg)")
        if save_path:
            self.pixmap.save(save_path, "PNG", 100)

    # -------------------------CONVERTING FUNCTIONS---------------------------

    def convert_cv_to_pixmap(self, cvImage):
        if self.cv2image_used:
            height, width, channel = self.cv2image.shape
            bytesPerLine = 3 * width
            qImage = QImage(
                cvImage.data,
                width,
                height,
                bytesPerLine,
                QImage.Format_RGB888).rgbSwapped()
            self.cv2image = cvImage

            return QPixmap(qImage)

    def convert_pixmap_to_mat(self, qImage: QImage):
        qImage = QImage(
            qImage.toImage().convertToFormat(
                QImage.Format_RGBX8888))
        ptr = qImage.bits()
        ptr.setsize(qImage.byteCount())
        cv_im_in = np.array(
            ptr, copy=True).reshape(
            qImage.height(), qImage.width(), 4)
        cv_im_in = cv2.cvtColor(cv_im_in, cv2.COLOR_BGRA2RGB)
        return cv_im_in

    # -------------------------ROTATE FUNCTIONS-------------------------------

    def flip_image(self, mode):  # 0 to horizontally, 1 to vertically
        if self.image_path:
            self.check_cvimage()

            new_image = cvf.flip_image(self.cv2image, mode)
            self.pixmap = self.convert_cv_to_pixmap(new_image)
            self.set_fixed_pixmap()

    def rotate_image(self, rotated=False):
        if self.image_path:
            self.check_cvimage()

            degrees = 90 if rotated else self.horizontalSliderRotation.value()

            new_image = cvf.rotate_image(self.cv2image, degrees)
            self.pixmap = self.convert_cv_to_pixmap(new_image)
            self.backup_cvimage.add_elem(self.cv2image)
            self.set_fixed_pixmap()

    # -------------------------HSV AND FILTER`S CHANGE FUNCTIONS--------------

    def change_hue(self):
        if self.cv2image_used:

            imageHSV = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2HSV)
            imageHSV[:, :, 0] = self.horizontalSliderHue.value()  # [h,s,v]

            self.cv2image = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)
            self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
            self.backup_cvimage.add_elem(self.cv2image)
            self.set_fixed_pixmap()

            self.backup_scrolls_list.add_elem(np.array([self.horizontalSliderHue.value(
            ), self.horizontalSliderContrast.value(), self.horizontalSliderBrightness.value()]))

    def change_contrast(self):
        if self.cv2image_used:
            imageHSV = cv2.cvtColor(self.cv2image, cv2.COLOR_BGR2HSV)

            contrast = self.horizontalSliderContrast.value() / 50
            res = cv2.addWeighted(imageHSV, contrast, imageHSV, 0, 0)
            self.cv2image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
            self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
            self.backup_cvimage.add_elem(self.cv2image)
            self.set_fixed_pixmap()

            self.backup_scrolls_list.add_elem(np.array([self.horizontalSliderHue.value(
            ), self.horizontalSliderContrast.value(), self.horizontalSliderBrightness.value()]))

    def change_brightness(self):
        if self.cv2image_used:
            self.cv2image = cvf.increase_brightness(
                self.cv2image, self.horizontalSliderBrightness.value())
            self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
            self.backup_cvimage.add_elem(self.cv2image)
            self.set_fixed_pixmap()

            self.backup_scrolls_list.add_elem(np.array([self.horizontalSliderHue.value(
            ), self.horizontalSliderContrast.value(), self.horizontalSliderBrightness.value()]))

    def choose_color_filter(self):
        if self.cv2image_used:
            mode = self.comboBoxFilters.currentText()
            tmpCV = None
            match(mode):
                case ('Sepia'): tmpCV = cvf.filterSepia(self.cv2image)
                case ('Invert'): tmpCV = cvf.filterInvert(self.cv2image)
                case ('Gray'): tmpCV = cvf.filterGray(self.cv2image)
                case ('Sharpen'): tmpCV = cvf.filterSharpen(self.cv2image)

                case _: return

            self.backup_cvimage.add_elem(tmpCV)
            self.pixmap = self.convert_cv_to_pixmap(tmpCV)
            self.set_fixed_pixmap()
            self.cv2image = tmpCV

    # -------------------------UNDO/REDO FUNCTIONS----------------------------

    def set_HSV_scrolls_values_from_backup(self):
        HSV_values = np.array(self.backup_scrolls_list.get_cur_version())
        self.horizontalSliderHue.setValue(HSV_values[0])
        self.horizontalSliderContrast.setValue(HSV_values[1])
        self.horizontalSliderBrightness.setValue(HSV_values[2])

    def event_undo(self):
        if self.image_path:
            self.check_cvimage()
            self.backup_scrolls_list.event_undo()
            self.set_HSV_scrolls_values_from_backup()

            self.backup_cvimage.event_undo()
            self.cv2image = self.backup_cvimage.get_cur_version()
            self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
            self.set_fixed_pixmap()
            self.setup_modded_label()

    def event_redo(self):
        if self.image_path:
            self.check_cvimage()
            self.backup_cvimage.event_redo()
            self.cv2image = self.backup_cvimage.get_cur_version()
            self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
            self.set_fixed_pixmap()

            self.backup_scrolls_list.event_redo()
            self.set_HSV_scrolls_values_from_backup()
            self.setup_modded_label()

    def image_clicked_event(self):
        if self.labelPhoto.selected_region and self.labelPhoto.get_cropping_bool():
            self.tmpRegion = self.labelPhoto.get_selected_region()  # crop
            self.pixmap = self.tmpRegion
            self.cv2image = self.convert_pixmap_to_mat(self.pixmap)
            self.setup_modded_label()

        elif self.labelPhoto.get_puttingText_bool():
            self.add_text_on_image()

        self.cv2image_used = True
        self.backup_cvimage.add_elem(self.cv2image)
        self.set_fixed_pixmap()

    # -------------------------TEXT FUNCTIONS---------------------------------

    def add_text_button_clicked(self):
        if self.image_path:
            # choose panel with text settings
            self.stackedWidget.setCurrentIndex(2)
            self.labelPhoto.is_putting_text = True
            self.labelPhoto.is_cropping = False

    def add_text_on_image(self):
        tmpCVimage = self.convert_pixmap_to_mat(self.pixmap)

        coefX = tmpCVimage.shape[0] / self.labelPhoto.height()
        coefY = tmpCVimage.shape[1] / self.labelPhoto.width()

        finalX = int(self.labelPhoto.get_x() * coefX)
        finalY = int(self.labelPhoto.get_y() * coefY)

        coords = finalX, finalY
        self.cv2image = cvf.put_text(tmpCVimage,
                                     textLine=self.textClass.getText(),
                                     coords=coords,
                                     textSize=self.textClass.getTextSize(),
                                     color=self.textClass.getTextColor())
        self.pixmap = self.convert_cv_to_pixmap(self.cv2image)
        self.set_fixed_pixmap()

    def crop_image(self):
        if self.image_path:
            self.labelPhoto.is_cropping = True
            self.labelPhoto.is_putting_text = False

    def input_text_event(self):
        self.textClass.setText(self.lineEditText.text())

    def change_text_size(self):
        self.textClass.setTextSize(self.comboTextSize.currentIndex() + 1)

    def choose_text_color(self):
        dialog = QColorDialog(self)
        color = dialog.getColor()
        colorRgb = color.getRgb()[:3]
        colorRgbReversed = colorRgb[::-1]
        self.buttonChooseColor.setStyleSheet(
            "QWidget { background-color: %s }" %
            color.name())
        self.textClass.setTextColor(colorRgbReversed)


# Initialize The App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style.qss').read_text())
    UIWindow = UI()
    app.exec_()
