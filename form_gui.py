# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 600)
        MainWindow.setMinimumSize(QtCore.QSize(820, 600))
        MainWindow.setMaximumSize(QtCore.QSize(820, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelPhoto = QtWidgets.QLabel(self.centralwidget)
        self.labelPhoto.setGeometry(QtCore.QRect(170, 100, 641, 471))
        self.labelPhoto.setFrameShape(QtWidgets.QFrame.Box)
        self.labelPhoto.setText("")
        self.labelPhoto.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPhoto.setObjectName("labelPhoto")
        self.buttonFlipHoriz = QtWidgets.QPushButton(self.centralwidget)
        self.buttonFlipHoriz.setGeometry(QtCore.QRect(140, 10, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonFlipHoriz.setFont(font)
        self.buttonFlipHoriz.setObjectName("buttonFlipHoriz")
        self.buttonOpenFile = QtWidgets.QPushButton(self.centralwidget)
        self.buttonOpenFile.setGeometry(QtCore.QRect(10, 10, 130, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonOpenFile.sizePolicy().hasHeightForWidth())
        self.buttonOpenFile.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonOpenFile.setFont(font)
        self.buttonOpenFile.setObjectName("buttonOpenFile")
        self.buttonFlipVertic = QtWidgets.QPushButton(self.centralwidget)
        self.buttonFlipVertic.setGeometry(QtCore.QRect(270, 10, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonFlipVertic.setFont(font)
        self.buttonFlipVertic.setObjectName("buttonFlipVertic")
        self.horizontalSliderHue = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderHue.setGeometry(QtCore.QRect(10, 110, 151, 22))
        self.horizontalSliderHue.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.horizontalSliderHue.setMaximum(255)
        self.horizontalSliderHue.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderHue.setObjectName("horizontalSliderHue")
        self.labelTextHue = QtWidgets.QLabel(self.centralwidget)
        self.labelTextHue.setGeometry(QtCore.QRect(10, 90, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTextHue.setFont(font)
        self.labelTextHue.setObjectName("labelTextHue")
        self.horizontalSliderSight = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderSight.setGeometry(QtCore.QRect(10, 160, 151, 22))
        self.horizontalSliderSight.setMaximum(255)
        self.horizontalSliderSight.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderSight.setObjectName("horizontalSliderSight")
        self.labelTextSight = QtWidgets.QLabel(self.centralwidget)
        self.labelTextSight.setGeometry(QtCore.QRect(10, 140, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTextSight.setFont(font)
        self.labelTextSight.setObjectName("labelTextSight")
        self.horizontalSliderValue = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderValue.setGeometry(QtCore.QRect(10, 210, 151, 22))
        self.horizontalSliderValue.setMaximum(255)
        self.horizontalSliderValue.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderValue.setObjectName("horizontalSliderValue")
        self.labelTextValue = QtWidgets.QLabel(self.centralwidget)
        self.labelTextValue.setGeometry(QtCore.QRect(10, 190, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTextValue.setFont(font)
        self.labelTextValue.setObjectName("labelTextValue")
        self.buttonSaveFile = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSaveFile.setGeometry(QtCore.QRect(10, 40, 130, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSaveFile.sizePolicy().hasHeightForWidth())
        self.buttonSaveFile.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonSaveFile.setFont(font)
        self.buttonSaveFile.setObjectName("buttonSaveFile")
        self.buttonCrop = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCrop.setGeometry(QtCore.QRect(400, 10, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonCrop.setFont(font)
        self.buttonCrop.setObjectName("buttonFlipCrop")
        self.labelTextRotation = QtWidgets.QLabel(self.centralwidget)
        self.labelTextRotation.setGeometry(QtCore.QRect(10, 270, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelTextRotation.setFont(font)
        self.labelTextRotation.setObjectName("labelTextRotation")
        self.horizontalSliderRotation = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderRotation.setGeometry(QtCore.QRect(10, 290, 151, 22))
        self.horizontalSliderRotation.setMaximum(90)
        self.horizontalSliderRotation.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderRotation.setObjectName("horizontalSliderRotation")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PhotoEditor"))
        self.buttonFlipHoriz.setText(_translate("MainWindow", "Flip Horizontally"))
        self.buttonOpenFile.setText(_translate("MainWindow", "Open File"))
        self.buttonFlipVertic.setText(_translate("MainWindow", "Flip Vertically"))
        self.labelTextHue.setText(_translate("MainWindow", "Hue"))
        self.labelTextSight.setText(_translate("MainWindow", "Sight"))
        self.labelTextValue.setText(_translate("MainWindow", "Value"))
        self.buttonSaveFile.setText(_translate("MainWindow", "Save File"))
        self.buttonCrop.setText(_translate("MainWindow", "Crop"))
        self.labelTextRotation.setText(_translate("MainWindow", "Rotation Degrees"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
