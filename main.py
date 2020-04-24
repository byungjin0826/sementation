from PyQt5.QtGui import *
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2 as cv
import numpy as np


form_class = uic.loadUiType('./ui/test1.ui')[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.originimage = None
        self.modifiedimage = None
        self.contourimage = None
        self.pixmap = None
        self.contours = None

        self.loadImageFromFile()
        self.filterImage()
        self.settingcontourSlide()
        self.imagenumberSlider.valueChanged.connect(self.loadImageFromFile)
        self.imagenumberSlider.valueChanged.connect(self.filterImage)
        self.thresholdSlider.valueChanged.connect(self.filterImage)
        self.thresholdSlider.valueChanged.connect(self.settingcontourSlide)
        self.contourSlider.valueChanged.connect(self.selectContour)


    def loadImageFromFile(self):
        root = './CT image/head-ct-hemorrhage/origin/'
        file_name = f'{str(self.imagenumberSlider.value()-1).rjust(3, "0")}.png'
        self.originimage = cv.imread(root+file_name)
        self.originimage = cv.cvtColor(self.originimage, cv.COLOR_BGR2RGB)
        self.originimage = cv.resize(self.originimage, (355, 435))
        h, w, c = self.originimage.shape
        qImg = QImage(self.originimage.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.originImage.setPixmap(pixmap)
        # self.originImage.resize(pixmap.width(), pixmap.height())
        self.originImage.show()

    def filterImage(self):
        self.modifiedimage = self.originimage
        self.modifiedimage = cv.cvtColor(self.modifiedimage, cv.COLOR_RGB2GRAY)
        threshold = self.thresholdSlider.value()
        _, self.modifiedimage = cv.threshold(self.modifiedimage, threshold, 255, cv.THRESH_BINARY)
        img = cv.cvtColor(self.modifiedimage, cv.COLOR_GRAY2RGB)
        h, w, c = img.shape
        qImg = QImage(img, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.modifiedImage.setPixmap(pixmap)
        self.originImage.resize(pixmap.width(), pixmap.height())
        self.modifiedImage.show()

    def settingcontourSlide(self):
        self.contours, _ = cv.findContours(self.modifiedimage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.contours = [x for x in self.contours if cv.contourArea(x) > 500]
        self.contourSlider.setMaximum(len(self.contours))

    def selectContour(self):
        n = self.contourSlider.value()
        contour = self.contours[n]
        img_rgb = cv.cvtColor(self.modifiedimage, cv.COLOR_GRAY2RGB)
        self.contourimage = cv.drawContours(img_rgb,
                                            [contour],
                                            0,  # 컨투어 라인 번호
                                            (0, 255, 0),  # 색상
                                            2)
        h, w, c = self.contourimage.shape
        qImg = QImage(self.contourimage, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.modifiedImage.setPixmap(pixmap)
        # self.originImage.resize(pixmap.width(), pixmap.height())
        self.modifiedImage.show()

    # def imageSelection(self):



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


# pyinstaller -w -F qtextbrowser_advanced.py