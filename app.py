import glob
import os
import sys
import threading
import multiprocessing
import time
from playsound import playsound
import serial
import serial.tools.list_ports
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *


# APP
#####################################################################################


class ImageAdDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advertisement")
        self.resize(600, 1024)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.checker)

    def checker(self, state):
        print(state)
        if state == 0:
            self.mediaPlayer.play()

    def keyPressEvent(self, event):
        if event.key() == 65:
            ui.BasicW.Weight_ip.clear()
            self.mediaPlayer.stop()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


######################################################################################


class VideoAdDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advertisement")
        self.resize(600, 1024)
        #######
        self.index = 0
        self.flag = 0
        self.clips = glob.glob(R'Videos\*.avi')
        self.filename = self.clips[0]
        #######
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.checker)

    def checker(self, state):
        if state == 0:
            self.next_on_track()

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.flag = 1
            self.index = 0
            self.filename = self.clips[0]
            self.mediaPlayer.stop()
            self.flag = 0
            ui.BasicW.Weight_ip.clear()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

    def video_run(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.filename)))
        self.mediaPlayer.play()

    def next_on_track(self):
        if self.flag == 0:
            if self.index != len(self.clips):
                try:
                    self.index += 1
                    self.filename = self.clips[self.index]
                except:
                    self.index = 0
                    self.filename = self.clips[self.index]
                self.video_run()


# 3


class BasicWindow(QMainWindow):
    def __init__(self):
        # Loading ui
        super().__init__()
        uic.loadUi("UI Files\English\Mainwindow.ui", self)
        # Button click events, set values
        self.Settings_Bt.clicked.connect(self.gotoMainMenu)
        self.Go_Bt.clicked.connect(self.gotoInsertScreen)
        self.Weight_ip.textEdited.connect(self.weight_checker)


    def weight_checker(self):
        try:
            if float(self.Weight_ip.text()) <= 5:
                if gv.SettingsInputs.value('Screensaver') == 'Videos':
                    time.sleep(2)
                    ui.widget.setCurrentIndex(ui.widgets_list.index(ui.vidAdW))
                    ui.vidAdW.video_run()
                if gv.SettingsInputs.value('Screensaver') == 'Images':
                    time.sleep(2)
                    ui.widget.setCurrentIndex(ui.widgets_list.index(ui.imgAdW))
                    ui.imgAdW.mediaPlayer.setMedia(QMediaContent(
                        QUrl.fromLocalFile("Saved videos\Img_SS.avi")))
                    ui.imgAdW.mediaPlayer.play()

        except:
            pass

    def gotoInsertScreen(self):
        try:
            if float(self.Weight_ip.text()) >= 5:
                self.Weight_ip.clear()
                ui.filename = insertcoin
                ui.Player.stop()
                ui.playmusic()
                ui.widget.setCurrentIndex(ui.widgets_list.index(ui.InsertW))
        except Exception as e:
            print(e)
            pass

    def gotoMainMenu(self):
        ui.mmW.setFocus()
        self.Weight_ip.clear()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.mmW))


############################################################################


class InsertWindow(QMainWindow):
    def __init__(self):
        # load ui
        super().__init__()
        uic.loadUi("UI Files\English\InsertWindow.ui", self)
        # button click events
        self.Back_Bt.clicked.connect(self.gotoWeightIPScreen)

    def keyPressEvent(self, event):

        if event.key() == 65:
            reply = QMessageBox.question(None, "Wish", "Do you want to display weight?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                ui.filename = background
                ui.Player.stop()
                ui.playmusic()
                ui.widget.setCurrentIndex(ui.widgets_list.index(ui.bmiW))
                ui.bmiW.countdown()

    def gotoWeightIPScreen(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


#############################################################################


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\MainMenuWindow.ui", self)
        self.Admin_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)
        # self.Password_ip.setEchoMode(QLineEdit.Password)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Admin_bt.clicked.connect(self.enterpassword)
        self.Login_bt.clicked.connect(self.gotoSettingsOptions)
        self.Cancel_bt.clicked.connect(self.cancel)
        self.Back_bt.clicked.connect(self.gotoBasicWindow)

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.Admin_bt.setVisible(True)

    def enterpassword(self):
        self.Password_label.setVisible(True)
        self.Password_ip.setVisible(True)
        self.Login_bt.setVisible(True)
        self.Cancel_bt.setVisible(True)

    def cancel(self):
        self.Password_ip.clear()
        self.Admin_bt.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)

    def gotoSettingsOptions(self):
        if self.Password_ip.text() == 'admin':
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))
        self.Password_ip.clear()

    def gotoBasicWindow(self):
        self.Admin_bt.setVisible(False)
        self.Password_ip.clear()
        self.Admin_bt.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


####################################################################################


class SettingsOptions(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\SettingsOptions.ui", self)
        self.Lang_cb.setCurrentText(str(gv.SettingsInputs.value('Language')))
        self.Ad_cb.setCurrentText(str(gv.SettingsInputs.value('Screensaver')))
        self.Signout_bt.clicked.connect(self.gotoBasicWindow)
        self.Setup_bt.clicked.connect(self.gotoSetupWindow)
        self.Ad_cb.currentTextChanged.connect(self.setAd)
        self.Lang_cb.currentTextChanged.connect(self.setLang)
        self.Weightcal_bt.clicked.connect(self.gotoWCWindow)
        self.Heightcal_bt.clicked.connect(self.gotoHCWindow)
        self.Sms_bt.clicked.connect(self.gotoSMSCWindow)
        self.Report_bt.clicked.connect(self.gotoRWindow)
        self.Diagnostic_bt.clicked.connect(self.gotoDiagWindow)
        self.Printsetup_bt.clicked.connect(self.gotoPSSWindow)

    def setAd(self, state):
        if state == 'Videos':
            gv.SettingsInputs.setValue('Screensaver', 'Videos')
        else:
            gv.SettingsInputs.setValue('Screensaver', 'Images')

    def setLang(self, state):
        if state == 'Tamil':
            gv.SettingsInputs.setValue('Language', 'Tamil')
        else:
            gv.SettingsInputs.setValue('Language', 'English')

    def gotoBasicWindow(self):
        ui.mmW.Admin_bt.setVisible(False)
        ui.mmW.Login_bt.setVisible(False)
        ui.mmW.Cancel_bt.setVisible(False)
        ui.mmW.Password_label.setVisible(False)
        ui.mmW.Password_ip.setVisible(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

    def gotoWCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.wcW))

    def gotoHCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.hcW))

    def gotoSMSCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.smscW))

    def gotoRWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.rW))

    def gotoDiagWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.dW))

    def gotoPSSWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.pssW))

    def gotoSetupWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.setupW))


########################################################################################

class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\SetupWindow.ui", self)
        self.Pos_cb.setCurrentText(
            str(gv.SettingsInputs.value('Print or SMS')))
        self.Wd_cb.setCurrentText(
            str(gv.SettingsInputs.value('Weight Display')))
        self.Back_bt.clicked.connect(self.gotoSettingsOptions_Back)
        self.Save_bt.clicked.connect(self.gotoSettingsOptions_Save)

    def gotoSettingsOptions_Back(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))

    def gotoSettingsOptions_Save(self):

        if self.Pos_cb.currentText() == 'Print only':
            gv.SettingsInputs.setValue('Print or SMS', 'Print only')
        elif self.Pos_cb.currentText() == 'SMS only':
            gv.SettingsInputs.setValue('Print or SMS', 'SMS only')
        else:
            gv.SettingsInputs.setValue("Print or SMS", 'Print and SMS')

        if self.Wd_cb.currentText() == 'Yes':
            gv.SettingsInputs.setValue('Weight Display', 'Yes')
        else:
            gv.SettingsInputs.setValue('Weight Display', 'No')

        self.gotoSettingsOptions_Back()


#######################################################################################


class WCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\WeightCalibrationWindow.ui", self)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


########################################################################################


class HCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\HeightCalibrationWindow.ui", self)
        self.Signout_bt.clicked.connect(self.gotoSettingsOptions)
        self.Ah_lb.setVisible(False)
        self.Ah_val.setVisible(False)
        self.Adc_lb.setVisible(False)
        self.Adc_val.setVisible(False)
        self.RefH_lb.setVisible(False)
        self.RefH_ip.setVisible(False)
        self.Close_bt.clicked.connect(self.hide)
        self.Set_bt.clicked.connect(self.show_params)

    def show_params(self):
        self.Ah_lb.setVisible(True)
        self.Ah_val.setVisible(True)
        self.Adc_lb.setVisible(True)
        self.Adc_val.setVisible(True)
        self.RefH_lb.setVisible(True)
        self.RefH_ip.setVisible(True)

    def hide(self):
        self.Ah_lb.setVisible(False)
        self.Ah_val.setVisible(False)
        self.Adc_lb.setVisible(False)
        self.Adc_val.setVisible(False)
        self.RefH_lb.setVisible(False)
        self.RefH_ip.setVisible(False)

    def gotoSettingsOptions(self):
        self.hide()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


############################################################################


class SMSCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\SMSConfigWindow.ui", self)
        self.Dc_bt.setEnabled(False)
        self.Send_bt.setEnabled(False)
        self.C_bt.clicked.connect(self.enable)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)

    def enable(self):
        self.Dc_bt.setEnabled(True)
        self.Send_bt.setEnabled(True)

    def gotoSettingsOptions(self):
        self.Dc_bt.setEnabled(False)
        self.Send_bt.setEnabled(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


##############################################################################


class RWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\ReportWindow.ui", self)
        self.Ok_bt.clicked.connect(self.gotoSettingsOptions)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


###############################################################################


class DiagWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\DiagnosticsWindow.ui", self)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)
        # O/P on buttons
        # self.op1_onbt.clicked.connect(self.on_op)
        self.op1_onbt.clicked.connect(lambda flag, i=1: self.on_op(flag, i))
        self.op2_onbt.clicked.connect(lambda flag, i=2: self.on_op(flag, i))
        self.op3_onbt.clicked.connect(lambda flag, i=3: self.on_op(flag, i))
        self.op4_onbt.clicked.connect(lambda flag, i=4: self.on_op(flag, i))
        self.op5_onbt.clicked.connect(lambda flag, i=5: self.on_op(flag, i))
        self.op6_onbt.clicked.connect(lambda flag, i=6: self.on_op(flag, i))
        self.op7_onbt.clicked.connect(lambda flag, i=7: self.on_op(flag, i))
        self.op8_onbt.clicked.connect(lambda flag, i=8: self.on_op(flag, i))
        # O/P off buttons
        self.op1_offbt.clicked.connect(lambda flag, i=1: self.off_op(flag, i))
        self.op2_offbt.clicked.connect(lambda flag, i=2: self.off_op(flag, i))
        self.op3_offbt.clicked.connect(lambda flag, i=3: self.off_op(flag, i))
        self.op4_offbt.clicked.connect(lambda flag, i=4: self.off_op(flag, i))
        self.op5_offbt.clicked.connect(lambda flag, i=5: self.off_op(flag, i))
        self.op6_offbt.clicked.connect(lambda flag, i=6: self.off_op(flag, i))
        self.op7_offbt.clicked.connect(lambda flag, i=7: self.off_op(flag, i))
        self.op8_offbt.clicked.connect(lambda flag, i=8: self.off_op(flag, i))

    def on_op(self, flag, i):

        if i == 1:
            self.op1_lb.setStyleSheet("background-color:green")
        if i == 2:
            self.op2_lb.setStyleSheet("background-color:green")
        if i == 3:
            self.op3_lb.setStyleSheet("background-color:green")
        if i == 4:
            self.op4_lb.setStyleSheet("background-color:green")
        if i == 5:
            self.op5_lb.setStyleSheet("background-color:green")
        if i == 6:
            self.op6_lb.setStyleSheet("background-color:green")
        if i == 7:
            self.op7_lb.setStyleSheet("background-color:green")
        if i == 8:
            self.op8_lb.setStyleSheet("background-color:green")

    def off_op(self, flag, i):

        if i == 1:
            self.op1_lb.setStyleSheet("background-color:red")
        if i == 2:
            self.op2_lb.setStyleSheet("background-color:red")
        if i == 3:
            self.op3_lb.setStyleSheet("background-color:red")
        if i == 4:
            self.op4_lb.setStyleSheet("background-color:red")
        if i == 5:
            self.op5_lb.setStyleSheet("background-color:red")
        if i == 6:
            self.op6_lb.setStyleSheet("background-color:red")
        if i == 7:
            self.op7_lb.setStyleSheet("background-color:red")
        if i == 8:
            self.op8_lb.setStyleSheet("background-color:red")

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


###############################################################################


class PSSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\PrintSlipSettingsWindow.ui", self)
        self.Yes_cb.clicked.connect(self.clicked_yes)
        self.No_cb.clicked.connect(self.clicked_no)
        self.Cancel_bt.clicked.connect(self.gotoSettingsOptions)

    def clicked_yes(self):
        self.No_cb.setChecked(False)

    def clicked_no(self):
        self.Yes_cb.setChecked(False)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


###############################################################################


class BMI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\English\BMIWindow.ui", self)
        self.needle_1.setHidden(True)
        self.needle_2.setHidden(True)
        self.needle_3.setHidden(True)
        self.needle_4.setHidden(True)
        self.needle_5.setHidden(True)
        self.secs = 10
        self.height.setText(self.get_height())
        self.weight.setText(self.get_weight())
        self.Result.setText(self.get_bmi())

    def get_height(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)

            self.Ht = str(ip.read(13))
            self.Ht = self.Ht[6:13]
            decode = self.Ht.split("-")
            self.Ht = decode[1]
            self.Ht = self.Ht[:len(self.Ht) - int(decode[0])] + \
                      "." + self.Ht[len(self.Ht) - int(decode[0]):]
        except:
            self.Ht = "180"
        return self.Ht

    def get_weight(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)
            self.Wt = str(ip.read(13))
            self.Wt = self.Wt[6:13]
            decode = self.Wt.split("-")  # [decimal places from right , value]
            self.Wt = decode[1]
            self.Wt = self.Wt[:len(self.Wt) - int(decode[0])] + \
                      "." + self.Wt[len(self.Wt) - int(decode[0]):]

        except:
            self.Wt = "75"

        return self.Wt

    def get_bmi(self):
        self.BMindex = str("{:.2f}".format(
            float(self.Ht) / ((float(self.Wt) / 100) ** 2)))

        if self.BMindex < "20":
            self.needle_1.setHidden(False)
        elif self.BMindex >= "20" and self.BMindex < "25":
            self.needle_2.setHidden(False)
        elif self.BMindex >= "25" and self.BMindex < "30":
            self.needle_3.setHidden(False)
        elif self.BMindex >= "30" and self.BMindex < "35":
            self.needle_4.setHidden(False)
        else:
            self.needle_5.setHidden(False)

        return self.BMindex

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.secs = 10
            self.timer.stop()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.posW))
            ui.posW.countdown()
        else:
            self.lb_timer_bmi.setText(str(self.secs))
            self.secs -= 1


##################################################################################

class POSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\PrintorSmsWindow.ui", self)
        self.secs = 10
        self.Print_bt.clicked.connect(self.Print)
        self.Sms_bt.clicked.connect(self.SMS)


    def Print(self):
        self.timer.stop()
        ui.filename = printM
        ui.Player.stop()
        ui.playmusic()
        self.timer_lb.setText("")
        time.sleep(5)
        ui.filename = background
        ui.Player.stop()
        ui.playmusic()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

    def SMS(self):
        self.secs = 10
        self.timer.stop()
        ui.filename = sms
        ui.Player.stop()
        ui.playmusic()
        self.timer_lb.setText("")
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.ssmsW))

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.timer_lb.setText(str(self.secs))
            self.secs = 10
            self.timer.stop()
            #################################
            ui.filename = printM
            ui.Player.stop()
            ui.playmusic()
            time.sleep(5)
            ui.filename = background
            ui.Player.stop()
            ui.playmusic()
            #######################################
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))
        else:
            self.timer_lb.setText(str(self.secs))
            self.secs -= 1


##################################################################################

class SendSMSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\SendSMSWindow.ui", self)
        self.Back_bt.clicked.connect(self.gotoPOSWindow)
        self.Send_bt.clicked.connect(self.finish)

    def gotoPOSWindow(self):
        ui.posW.timer.start()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.posW))

    def finish(self):
        ui.filename = background
        ui.Player.stop()
        ui.playmusic()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


###################################################################################
###################################################################################

class UI():
    def __init__(self):
        self.widget = QStackedWidget()

        # Instances of windows
        self.BasicW = BasicWindow()
        self.InsertW = InsertWindow()
        self.vidAdW = VideoAdDisplayWindow()
        self.mmW = MainMenu()
        self.OptionsW = SettingsOptions()
        self.setupW = SetupWindow()
        self.wcW = WCWindow()
        self.hcW = HCWindow()
        self.smscW = SMSCWindow()
        self.rW = RWindow()
        self.dW = DiagWindow()
        self.pssW = PSSWindow()
        self.bmiW = BMI()
        self.posW = POSWindow()
        self.ssmsW = SendSMSWindow()
        self.imgAdW = ImageAdDisplayWindow()

        # widgets list
        self.widgets_list = [self.BasicW, self.InsertW, self.vidAdW, self.mmW,
                             self.OptionsW, self.setupW, self.wcW, self.hcW,
                             self.smscW, self.rW, self.dW, self.pssW, self.bmiW,
                             self.posW, self.ssmsW, self.imgAdW]

        for i in self.widgets_list:
            self.widget.addWidget(i)

        # set width and height
        self.widget.setFixedHeight(1024)
        self.widget.setFixedWidth(600)

        ############
        self.filename = background
        self.Player = QMediaPlayer()
        self.playmusic()
        self.t = threading.Thread(target=self.loop)
        self.t.daemon = True
        self.t.start()
        #############
        self.widget.show()

    def playmusic(self):
        url = QUrl.fromLocalFile(self.filename)
        content = QMediaContent(url)
        self.Player.setMedia(content)
        self.Player.play()

    def loop(self):
        while True:
            if self.Player.state() == 0:
                self.Player.play()
                time.sleep(1.5)




###################################################################################
###################################################################################


class GV():
    def __init__(self):
        self.getSettingsValues()

    def getSettingsValues(self):
        self.SettingsInputs = QSettings('Smart BMI', 'SettingsWindow')


###################################################################################
###################################################################################


gv = GV()
os.system('python img2SS.py')

###################################
###################################
#initialize
background = 'Sounds/Background.wav'
insertcoin = 'Sounds/InsertCoin.mp3'
printM = 'Sounds/Print.mp3'
sms = 'Sounds/sms.mp3'

# Application
app = QApplication(sys.argv)
ui = UI()
app.exec_()

###################################
###################################
