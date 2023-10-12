import PyQt5

from PyQt5 import QtWidgets

class TextEdit:
    def __init__(self):
        self.text = ""
        self.textSize = 1
        self.textColor = ""

    def setText(self, line: str):
        self.text = line

    def setTextSize(self, sz: int):
        self.text = sz

    def setTextColor(self, clr):
        self.textColor = clr

    def getText(self):
        return self.text

    def getTextSize(self):
        return self.textSize

    def getTextColor(self):
        return self.textColor

