import PyQt5

from PyQt5 import QtWidgets

class TextEdit:
    def __init__(self):
        self.text = "Hello"
        self.textSize = 1
        self.textColor = (0,0,0)

    def setText(self, line: str):
        self.text = line

    def setTextSize(self, sz: int):
        self.textSize = sz

    def setTextColor(self, clr):
        self.textColor = clr

    def getText(self):
        return self.text

    def getTextSize(self):
        return self.textSize

    def getTextColor(self):
        return self.textColor

