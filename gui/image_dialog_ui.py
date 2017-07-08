# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageDialog(object):
    def setupUi(self, ImageDialog):
        ImageDialog.setObjectName("ImageDialog")
        ImageDialog.resize(791, 670)
        self.windowTitle = QtWidgets.QLabel(ImageDialog)
        self.windowTitle.setGeometry(QtCore.QRect(0, 0, 791, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.windowTitle.setFont(font)
        self.windowTitle.setAutoFillBackground(True)
        self.windowTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.windowTitle.setObjectName("windowTitle")
        self.image = QtWidgets.QWidget(ImageDialog)
        self.image.setGeometry(QtCore.QRect(0, 140, 791, 531))
        self.image.setAutoFillBackground(True)
        self.image.setObjectName("image")
        self.btn_expose = QtWidgets.QPushButton(ImageDialog)
        self.btn_expose.setGeometry(QtCore.QRect(10, 50, 81, 81))
        self.btn_expose.setObjectName("btn_expose")
        self.btn_crosshair = QtWidgets.QPushButton(ImageDialog)
        self.btn_crosshair.setGeometry(QtCore.QRect(340, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_crosshair.setFont(font)
        self.btn_crosshair.setObjectName("btn_crosshair")
        self.groupBox_2 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(710, 40, 71, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.btn_strechLow = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechLow.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.btn_strechLow.setObjectName("btn_strechLow")
        self.btn_strechMid = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechMid.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.btn_strechMid.setObjectName("btn_strechMid")
        self.btn_strechHigh = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechHigh.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.btn_strechHigh.setObjectName("btn_strechHigh")
        self.groupBox_3 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(630, 40, 71, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.btn_size25 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size25.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.btn_size25.setObjectName("btn_size25")
        self.btn_size50 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size50.setGeometry(QtCore.QRect(10, 40, 51, 21))
        self.btn_size50.setObjectName("btn_size50")
        self.btn_size100 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size100.setGeometry(QtCore.QRect(10, 60, 51, 21))
        self.btn_size100.setObjectName("btn_size100")
        self.btn_solve = QtWidgets.QPushButton(ImageDialog)
        self.btn_solve.setGeometry(QtCore.QRect(340, 100, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_solve.setFont(font)
        self.btn_solve.setObjectName("btn_solve")
        self.groupBox_4 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_4.setGeometry(QtCore.QRect(540, 40, 81, 91))
        self.groupBox_4.setObjectName("groupBox_4")
        self.btn_colorGrey = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorGrey.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.btn_colorGrey.setObjectName("btn_colorGrey")
        self.btn_colorCool = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorCool.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.btn_colorCool.setObjectName("btn_colorCool")
        self.btn_colorRainbow = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorRainbow.setGeometry(QtCore.QRect(10, 60, 71, 21))
        self.btn_colorRainbow.setObjectName("btn_colorRainbow")
        self.btn_startContExposures = QtWidgets.QPushButton(ImageDialog)
        self.btn_startContExposures.setGeometry(QtCore.QRect(100, 50, 81, 81))
        self.btn_startContExposures.setObjectName("btn_startContExposures")
        self.btn_stopContExposures = QtWidgets.QPushButton(ImageDialog)
        self.btn_stopContExposures.setGeometry(QtCore.QRect(190, 50, 81, 81))
        self.btn_stopContExposures.setObjectName("btn_stopContExposures")
        self.label_82 = QtWidgets.QLabel(ImageDialog)
        self.label_82.setGeometry(QtCore.QRect(340, 40, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_82.setFont(font)
        self.label_82.setObjectName("label_82")
        self.line_14 = QtWidgets.QFrame(ImageDialog)
        self.line_14.setGeometry(QtCore.QRect(390, 40, 31, 21))
        self.line_14.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setObjectName("line_14")
        self.btn_selectClose = QtWidgets.QPushButton(ImageDialog)
        self.btn_selectClose.setGeometry(QtCore.QRect(760, 0, 31, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_selectClose.setFont(font)
        self.btn_selectClose.setObjectName("btn_selectClose")
        self.cross4 = QtWidgets.QFrame(ImageDialog)
        self.cross4.setGeometry(QtCore.QRect(395, 420, 21, 241))
        self.cross4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross4.setFrameShape(QtWidgets.QFrame.VLine)
        self.cross4.setObjectName("cross4")
        self.cross2 = QtWidgets.QFrame(ImageDialog)
        self.cross2.setGeometry(QtCore.QRect(395, 149, 21, 241))
        self.cross2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross2.setFrameShape(QtWidgets.QFrame.VLine)
        self.cross2.setObjectName("cross2")
        self.cross1 = QtWidgets.QFrame(ImageDialog)
        self.cross1.setGeometry(QtCore.QRect(10, 395, 381, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cross1.setFont(font)
        self.cross1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross1.setFrameShape(QtWidgets.QFrame.HLine)
        self.cross1.setObjectName("cross1")
        self.cross3 = QtWidgets.QFrame(ImageDialog)
        self.cross3.setGeometry(QtCore.QRect(420, 395, 361, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cross3.setFont(font)
        self.cross3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross3.setFrameShape(QtWidgets.QFrame.HLine)
        self.cross3.setObjectName("cross3")

        self.retranslateUi(ImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ImageDialog)

    def retranslateUi(self, ImageDialog):
        _translate = QtCore.QCoreApplication.translate
        ImageDialog.setWindowTitle(_translate("ImageDialog", "Imaging Window"))
        self.windowTitle.setText(_translate("ImageDialog", "Image Window"))
        self.btn_expose.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single exposure</p></body></html>"))
        self.btn_expose.setText(_translate("ImageDialog", "Expose\n"
"single\n"
"Shot"))
        self.btn_crosshair.setText(_translate("ImageDialog", "Crosshairs"))
        self.groupBox_2.setTitle(_translate("ImageDialog", "Strech"))
        self.btn_strechLow.setText(_translate("ImageDialog", "Low"))
        self.btn_strechMid.setText(_translate("ImageDialog", "Mid"))
        self.btn_strechHigh.setText(_translate("ImageDialog", "High"))
        self.groupBox_3.setTitle(_translate("ImageDialog", "Zoom"))
        self.btn_size25.setText(_translate("ImageDialog", "25%"))
        self.btn_size50.setText(_translate("ImageDialog", "50%"))
        self.btn_size100.setText(_translate("ImageDialog", "100%"))
        self.btn_solve.setText(_translate("ImageDialog", "Solve"))
        self.groupBox_4.setTitle(_translate("ImageDialog", "Colors"))
        self.btn_colorGrey.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme black /white</p></body></html>"))
        self.btn_colorGrey.setText(_translate("ImageDialog", "Grey"))
        self.btn_colorCool.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme red/blue</p></body></html>"))
        self.btn_colorCool.setText(_translate("ImageDialog", "Cool"))
        self.btn_colorRainbow.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme rainbow</p></body></html>"))
        self.btn_colorRainbow.setText(_translate("ImageDialog", "Rainbow"))
        self.btn_startContExposures.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Starting taking continously exposures</p></body></html>"))
        self.btn_startContExposures.setText(_translate("ImageDialog", "Start\n"
"cont.\n"
"Exposures"))
        self.btn_stopContExposures.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Stopping taking continously exposures</p></body></html>"))
        self.btn_stopContExposures.setText(_translate("ImageDialog", "Stop\n"
"cont.\n"
"Exposures"))
        self.label_82.setText(_translate("ImageDialog", "Views"))
        self.btn_selectClose.setToolTip(_translate("ImageDialog", "Sets dual tracking on / off"))
        self.btn_selectClose.setText(_translate("ImageDialog", "X"))

