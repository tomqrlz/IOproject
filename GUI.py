from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal
from peopleCounter import analyze, saveVideo, saveLogs
import time
from os import startfile


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 300)
        self.pushButton1 = QtWidgets.QPushButton(MainWindow)
        self.pushButton1.setGeometry(QtCore.QRect(30, 200, 100, 32))
        self.pushButton1.setStyleSheet("background-color:red;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton1.setObjectName("pushButton1")

        self.pushButton2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton2.setGeometry(QtCore.QRect(130, 200, 100, 32))
        self.pushButton2.setStyleSheet("background-color:green;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton2.setObjectName("pushButton2")

        self.pushButton3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton3.setGeometry(QtCore.QRect(230, 200, 100, 32))
        self.pushButton3.setStyleSheet("background-color:pink;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton3.setObjectName("pushButton3")

        self.pushButton4 = QtWidgets.QPushButton(MainWindow)
        self.pushButton4.setGeometry(QtCore.QRect(330, 200, 100, 32))
        self.pushButton4.setStyleSheet("background-color:purple;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton4.setObjectName("pushButton4")

        self.pushButton5 = QtWidgets.QPushButton(MainWindow)
        self.pushButton5.setGeometry(QtCore.QRect(130, 250, 100, 32))
        self.pushButton5.setStyleSheet("background-color:blue;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton5.setObjectName("pushButton5")

        self.pushButton6 = QtWidgets.QPushButton(MainWindow)
        self.pushButton6.setGeometry(QtCore.QRect(230, 250, 100, 32))
        self.pushButton6.setStyleSheet("background-color:blue;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       "")
        self.pushButton6.setObjectName("pushButton6")



        self.pbar = QtWidgets.QProgressBar(MainWindow)
        self.pbar.setGeometry(50, 100, 360, 25)
        self.pbar.setMaximum(100)
        self.pbar.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KOX programik"))
        self.pushButton1.setText((_translate("MainWindow", "LOAD")))
        self.pushButton1.clicked.connect(self.LoadHandler)
        self.pushButton2.setText(_translate("MainWindow", "ANALYZE"))
        self.pushButton2.clicked.connect(self.AnalyzeVideo)
        self.pushButton3.setText(_translate("MainWindow", "SAVE"))
        self.pushButton3.clicked.connect(self.SaveVideo)
        self.pushButton4.setText(_translate("MainWindow", "SAVE LOGS"))
        self.pushButton4.clicked.connect(self.SaveLogs)
        self.pushButton5.setText(_translate("MainWindow", "PLAY"))
        self.pushButton5.clicked.connect(self.PlayVideo)
        self.pushButton6.setText(_translate("MainWindow", "READ LOGS"))
        self.pushButton6.clicked.connect(self.ReadLogs)


    def LoadHandler(self):
        if GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please weit...")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        else:
            self.OpenDialogBox()

    def OpenDialogBox(self):
        filename = QFileDialog.getOpenFileName()
        global GlobalPath, GlobalStatus, GlobalStatusLogs, GlobalOutput, GlobalOutputLogs

        if filename[0].endswith(".mp4") == True or filename[0].endswith(".avi") == True:
            GlobalPath = filename[0]
            GlobalStatus = "Not Analyzed"
            GlobalStatusLogs = "Not Saved"
            if GlobalOutput != "":
                GlobalOutput = ""
            if GlobalOutputLogs != "":
                GlobalOutputLogs = ""
            self.pbar.setFormat("Waiting...")
            self.pbar.setValue(0)

        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load mp4 or avi file")
            msg.setWindowTitle("Kox programik")
            msg.exec()

    def AnalyzeVideo(self):
        global GlobalPath, GlobalStatus, GlobalOutput, frameList, W, H, fps
        if GlobalPath == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load file to analyze")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus == "Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Video already analyzed")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please wait...")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus != "" and GlobalStatus == "Not Analyzed":
            GlobalStatus = "Analyzing"
            self.StartProgressBar()
            frameList, W, H, fps = analyze(GlobalPath)
            GlobalStatus = "Analyzed"

    def PlayVideo(self):
        if GlobalStatus == "Saved":
            startfile(f"{GlobalOutput}")
        elif GlobalStatus == "Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please save file to play video")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalPath == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load file to analyze")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please wait...")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalPath != "" and GlobalStatus == "Not Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please analyze video")
            msg.setWindowTitle("Kox programik")
            msg.exec()

    def ReadLogs(self):
        if GlobalStatusLogs == "Logs Saved":
            startfile(f"{GlobalOutputLogs}")
        elif GlobalStatusLogs == "Not Saved" and (GlobalStatus == "Analyzed" or GlobalStatus == "Saved"):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please save logs to read them")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalPath == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load file to analyze")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please wait...")
            msg.setWindowTitle("Kox programik")
            msg.exec()
        elif GlobalPath != "" and GlobalStatus == "Not Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please analyze video")
            msg.setWindowTitle("Kox programik")
            msg.exec()

    def SaveVideo(self):
        global GlobalPath, GlobalStatus, GlobalOutput, frameList, W, H, fps

        if GlobalPath == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load file to analyze")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalPath != "" and GlobalStatus == "Not Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please analyze video")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please wait...")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus == "Analyzed":
            fileName, _ = QFileDialog.getSaveFileName(None, "Save File", "",
                                                      ("mp4 File (*.mp4);;avi File (*.avi);;All Files (*)"))

            if fileName != "":
                GlobalOutput = fileName
                saveVideo(GlobalOutput, frameList, W, H, fps, GlobalPath)
                GlobalStatus = "Saved"

        elif GlobalStatus == "Saved":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Analyzed video already saved here: " + GlobalOutput)
            msg.setWindowTitle("Kox programik")
            msg.exec()

    def SaveLogs(self):
        global GlobalStatus, GlobalStatusLogs, GlobalOutputLogs

        if GlobalPath == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please load file to analyze")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalPath != "" and GlobalStatus == "Not Analyzed":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please analyze video")
            msg.setWindowTitle("Kox programik")
            msg.exec()

        elif GlobalStatus == "Analyzing":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Please wait...")
            msg.setWindowTitle("Kox programik")
            msg.exec()


        elif GlobalStatusLogs == "Not Saved" and (GlobalStatus == "Analyzed" or GlobalStatus == "Saved"):
            logsFileName, _ = QFileDialog.getSaveFileName(None, "Save Logs", "",
                                                          ("Log File (*.log);;All Files (*)"))
            if logsFileName != "":
                GlobalOutputLogs = logsFileName
                saveLogs(GlobalOutputLogs)
                GlobalStatusLogs = "Logs Saved"

        elif GlobalStatusLogs == "Logs Saved":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Warning!")
            msg.setInformativeText("Logs already saved here: " + GlobalOutputLogs)
            msg.setWindowTitle("Kox programik")
            msg.exec()

    def IncreaseProgress(self, val):
        self.pbar.setValue(val % 100)
        self.pbar.setFormat("Analyzing")
        if val == 987654321:
            self.pbar.setFormat("Analysis is done!")
            self.pbar.setValue(100)

    def StartProgressBar(self):
        self.thread = ThreadClass()
        self.thread.my_signal.connect(self.IncreaseProgress)
        self.thread.start()


class ThreadClass(QtCore.QThread):
    my_signal = pyqtSignal(int)
    global GlobalStatus
    def run(self):
        ctr = 0
        while True:
            ctr += 1
            time.sleep(1)
            self.my_signal.emit(ctr)
            if GlobalStatus == "Analyzed":
                self.my_signal.emit(987654321)
                break


if __name__ == "__main__":
    import sys

    GlobalPath = ""
    GlobalStatus = "Not Analyzed"
    GlobalStatusLogs = "Not Saved"
    GlobalOutput = ""
    GlobalOutputLogs = ""
    frameList = []
    W = 0
    H = 0
    fps = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
