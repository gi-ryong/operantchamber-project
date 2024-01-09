# 프로그램 제작자: gi-ryong son
# 작성일: 2023-11 ~ 2023-12


import sys                              
from PyQt5.QtWidgets import *           # PyQt5 사용하기 위한 것
from PyQt5 import uic                   # ui 파일을 직접 이용하기 위한 것
from PyQt5.QtGui import *
import serial.tools.list_ports
import time
import os
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget
import subprocess
from secondwindow import secondwindow as SecondWindowClass
import pickle
import numpy
import pandas as pd
from PyQt5.QtGui import QIcon
import threading
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt  



form_class = uic.loadUiType("port.ui")[0]

nnum = 0  # 여기에 선언하면 전역변수

ctrl_c = b'\x03'




class WindowClass(QMainWindow, form_class):
    
    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #################### X버튼 막기 ########################
        flags = self.windowFlags()
        flags &= ~Qt.WindowMaximizeButtonHint  # 최대화 버튼 비활성화
        flags &= ~Qt.WindowCloseButtonHint     # 닫기 버튼 비활성화
        self.setWindowFlags(flags)  
        #######################################################
        
        
        
        self.setWindowTitle("Operant_Chamber_Ver 1.0")
        self.setWindowIcon(QIcon("Scitech_Korea.png"))
        
        
        
        

        
        
        self.statusbar = QStatusBar(self)   # 상태바 객체 생성
        self.setStatusBar(self.statusbar)
        
        self.statusbar.setStyleSheet('background-color: #d45151; ')
        
        
        self.statusbar.showMessage("Ready to connect")  # 상태바 Ready to connect 표시
        
        self.btn1_clicked()
        
        
        self.btn.clicked.connect(lambda: (self.btn_clicked(), self.btn1_clicked()))
        self.port_done.clicked.connect(self.port_done_btn)
        self.start.clicked.connect(self.start_btn_)
        self.end.clicked.connect(self.end_btn_)
        self.exit.clicked.connect(self.exit_btn)
        self.datawindow.clicked.connect(self.button_Second)
        self.yes_btn.clicked.connect(self.toggle_radio_buttons)
        self.no_btn.clicked.connect(self.toggle_radio_buttons)
        self.clear_btn.clicked.connect(self.data_clear)
        self.save_btn.clicked.connect(self.save_data)
        # self.disconnecting_btn.clicked.connect(self.Disconnecting)
        
        
        
        self.USB_name = 'USER1'        # USB 이름
        self.ser = None
        self.stop_receiving_data = False
        # self.img_status = False
        self.must_touch_trials_value = None
        self.trial_done_detected = False
        self.trial_starts_value = None
        self.start_status = False
        self.restart=False
        
        self.start.setEnabled(False)  # 시작 버튼 비활성화
        self.end.setEnabled(False)
        
        self.port_done.setStyleSheet('background-color: #d4cb51; ')
        self.exit.setStyleSheet('background-color: #ff7369; ')

        
        self.yes_btn.setAutoExclusive(False)
        self.no_btn.setAutoExclusive(False)
        
        self.img_box.setEnabled(False)
        self.experiment_input.setReadOnly(True)
        self.reward_input.setReadOnly(True)
        self.hav2_input.setReadOnly(True)
        self.touch_input.setReadOnly(True)
        self.ITI_input.setReadOnly(True)
        
        self.yes_btn.setEnabled(False)
        self.no_btn.setEnabled(False)
        
        self.change_circle_color(QColor(255, 0, 0))  # 빨강으로 변경
        self.statusbar.setStyleSheet('background-color: #ff0000; ')
        
        self.img_change_circle_color(QColor(0, 0, 0))  
        self.experiment_change_circle_color(QColor(0, 0, 0))  
        self.reward_change_circle_color(QColor(0, 0, 0))  
        self.hav2_change_circle_color(QColor(0, 0, 0))  
        self.touch_change_circle_color(QColor(0, 0, 0))  
        self.ITI_change_circle_color(QColor(0, 0, 0))  
        self.video_change_circle_color(QColor(0, 0, 0))  
        
        
        self.experiment_input_original_style = self.experiment_input.styleSheet()
        self.reward_input_original_style = self.reward_input.styleSheet()
        self.hav2_input_original_style = self.hav2_input.styleSheet()
        self.touch_input_original_style = self.touch_input.styleSheet()
        self.ITI_input_original_style = self.ITI_input.styleSheet()
        
        self.enable_st()
        
        self.video_text.setStyleSheet('background-color: #d9d7d7;  ')
        self.ITI_text.setStyleSheet('background-color: #d9d7d7;  ')
        self.text.setStyleSheet('background-color: #d9d7d7;  ')
        
        
        
    def reset_style(self):
        # 초기 스타일로 돌리기
        self.experiment_input.setStyleSheet(self.experiment_input_original_style)
        self.reward_input.setStyleSheet(self.reward_input_original_style)
        self.hav2_input.setStyleSheet(self.hav2_input_original_style)
        self.touch_input.setStyleSheet(self.touch_input_original_style)
        self.ITI_input.setStyleSheet(self.ITI_input_original_style)
            
    ###################################################################################################### 
          
            
        
        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.circle_color)
        painter.setBrush(self.circle_color)
        painter.drawEllipse(390, 40, 15, 15)
        
        painter.setPen(self.img_circle_color)
        painter.setBrush(self.img_circle_color)
        painter.drawEllipse(270, 110, 10, 10)
        
        painter.setPen(self.experiment_circle_color)
        painter.setBrush(self.experiment_circle_color)
        painter.drawEllipse(270, 160, 10, 10)
        
        painter.setPen(self.reward_circle_color)
        painter.setBrush(self.reward_circle_color)
        painter.drawEllipse(270, 210, 10, 10)
        
        painter.setPen(self.hav2_circle_color)
        painter.setBrush(self.hav2_circle_color)
        painter.drawEllipse(270, 260, 10, 10)
        
        painter.setPen(self.touch_circle_color)
        painter.setBrush(self.touch_circle_color)
        painter.drawEllipse(270, 310, 10, 10)
        
        painter.setPen(self.ITI_circle_color)
        painter.setBrush(self.ITI_circle_color)
        painter.drawEllipse(270, 360, 10, 10)
        
        painter.setPen(self.video_circle_color)
        painter.setBrush(self.video_circle_color)
        painter.drawEllipse(270, 410, 10, 10)
        
    # def img_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.img_circle_color)
    #     painter.setBrush(self.img_circle_color)
    #     painter.drawEllipse(270, 110, 15, 15)
        
        
    # def experiment_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.experiment_circle_color)
    #     painter.setBrush(self.experiment_circle_color)
    #     painter.drawEllipse(270, 160, 15, 15)
        
        
    # def reward_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.reward_circle_color)
    #     painter.setBrush(self.reward_circle_color)
    #     painter.drawEllipse(270, 210, 15, 15)
        
        
    # def hav2_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.hav2_circle_color)
    #     painter.setBrush(self.hav2_circle_color)
    #     painter.drawEllipse(270, 260, 15, 15)
        
        
    # def touch_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.touch_circle_color)
    #     painter.setBrush(self.touch_circle_color)
    #     painter.drawEllipse(270, 310, 15, 15)     
        
    # def ITI_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.ITI_circle_color)
    #     painter.setBrush(self.ITI_circle_color)
    #     painter.drawEllipse(270, 360, 15, 15)        
        
        
    # def video_paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(self.video_circle_color)
    #     painter.setBrush(self.video_circle_color)
    #     painter.drawEllipse(270, 410, 15, 15)          
        
    def change_circle_color(self, color):
        self.circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
        
    def img_change_circle_color(self, color):
        self.img_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def experiment_change_circle_color(self, color):
        self.experiment_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def reward_change_circle_color(self, color):
        self.reward_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def hav2_change_circle_color(self, color):
        self.hav2_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def touch_change_circle_color(self, color):
        self.touch_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def ITI_change_circle_color(self, color):
        self.ITI_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    def video_change_circle_color(self, color):
        self.video_circle_color = color
        self.update()  # GUI 업데이트
        QApplication.processEvents()
        
    
        
        
    def btn_clicked(self):
        self.port_list.setEnabled(True)
        global nnum
        nnum = nnum + 1
        self.port_list.addItem("COM" + str(nnum))

    def btn1_clicked(self):
        self.port_list.clear()
        ports = serial.tools.list_ports.comports()

        available_ports = []
        for p in ports:
            try:
                port_number = int(p.device[3:])  # "COMx"에서 숫자 부분만 추출
                available_ports.append((port_number, p.device))
            except ValueError:
                pass

        if len(available_ports) > 0:
            available_ports.sort()  # 숫자 기준으로 오름차순으로 정렬
            for _, aa in available_ports:
                self.port_list.addItem(aa)
                
    def port_done_btn(self):
        
        
        self.trial_done_detected = False
        self.restart=False
        self.ser = None
         
        try:
            
            ser = serial.Serial(self.port_list.currentText(), 115200,timeout=1, stopbits=serial.STOPBITS_ONE)
            self.ser = ser
            print("성공")
            
            self.pi_login()
            
            
            
            
            
            if not self.USB():
                QMessageBox.critical(self, "경고", "USB를 연결하세요. \n또는 Port 번호를 확인하세요.")
                

            else:
            # if self.img_status == True:
                
                
                self.run()
                
                
                
                
                        
        except serial.SerialException as e:
            print(f"Failed to open the serial port: {e}")
            print(type(self.port_list.currentText()), self.port_list.currentText())
            self.port_done.setStyleSheet('background-color: #ff6666; ')
            self.port_done.setText("재연결")
            self.ser = None
            self.restart = True

    def start_btn_(self):
        if self.ser:
            
            self.data_clear()
            
            self.restart = True
            
            self.stop_receiving_data = False
            experiment_id = self.experiment_input.text()
            rd = self.reward_input.text()
            habv2_trials = self.hav2_input.text()
            must_touch_trials = self.touch_input.text()
            ITI = self.ITI_input.text()
            visual_select = self.img_box.currentText()

            missing_fields = []  # 경고 메시지

            if not experiment_id:
                missing_fields.append("experiment_id")
            if not rd:
                missing_fields.append("reward duration")
            if not habv2_trials:
                missing_fields.append("habv2 trials")
            if not must_touch_trials:
                missing_fields.append("must touch trials")
            if not ITI:
                missing_fields.append("ITI")
            if not visual_select:
                missing_fields.append("visual_select")  
            

            if missing_fields:
                QMessageBox.critical(self, "경고", f"{', '.join(missing_fields)}을(를) 입력하세요.")
                return
            
            if not self.is_numeric(rd) :
                QMessageBox.critical(self, "경고", "reward duration은 숫자만 입력하세요.")
                return
            
            if not habv2_trials.isdigit() :
                QMessageBox.critical(self, "경고", "habv2_trials은 정수만 입력하세요.")
                return
            
            if not must_touch_trials.isdigit() :
                QMessageBox.critical(self, "경고", "must_touch_trials은 정수만 입력하세요.")
                return
            
            if not self.is_numeric(ITI) :
                QMessageBox.critical(self, "경고", "ITI은 숫자만 입력하세요.")
                return
            


            video = None  # 선택된 라디오 버튼을 추적하기 위한 변수
            if self.yes_btn.isChecked():
                video = 'y'
            elif self.no_btn.isChecked():
                video = 'n'
                self.video_text.insertPlainText("Not recording video")

            if video is None:
                QMessageBox.critical(self, "경고", "비디오 녹화 여부를 선택하세요.")
                return

            if experiment_id and rd and habv2_trials and must_touch_trials and ITI and visual_select and video is not None:
                self.start_status = True

            experiment_id = experiment_id.encode('utf-8')
            rd = rd.encode('utf-8')
            habv2_trials = habv2_trials.encode('utf-8')
            must_touch_trials = must_touch_trials.encode('utf-8')
            video = video.encode('utf-8')
            ITI = ITI.encode('utf-8')
            visual_select = visual_select.encode('utf-8')

            self.text.insertPlainText('experiment_id : ' + experiment_id.decode('utf-8') + '\n')
            self.text.insertPlainText('reward duration : ' + rd.decode('utf-8') + '\n')
            self.text.insertPlainText('habv2 trials : ' + habv2_trials.decode('utf-8') + '\n')
            self.text.insertPlainText('must touch trials : ' + must_touch_trials.decode('utf-8') + '\n')
            
            self.text.insertPlainText('video recording : ' + video.decode('utf-8') + '\n')
            self.text.insertPlainText('ITI : ' + ITI.decode('utf-8') + 'sec' + '\n')
            self.text.insertPlainText('visual_select : ' + visual_select.decode('utf-8') + '\n\n')


             
         
          
         
            
         

        
            self.send_and_receive("experiment id:", experiment_id)
            self.img_change_circle_color(QColor(0, 255, 0)) 
            self.send_and_receive("reward duration:", rd)
            self.experiment_change_circle_color(QColor(0, 255, 0)) 
            self.send_and_receive("habv2 trials:", habv2_trials)
            self.reward_change_circle_color(QColor(0, 255, 0))
            self.send_and_receive("must touch trials:", must_touch_trials)
            self.hav2_change_circle_color(QColor(0, 255, 0)) 
            
            self.send_and_receive("video recording?(y/n):", video)
            self.touch_change_circle_color(QColor(0, 255, 0)) 
            self.send_and_receive("ITI:", ITI)
            self.ITI_change_circle_color(QColor(0, 255, 0)) 
            self.send_and_receive("img:", visual_select)
            self.video_change_circle_color(QColor(0, 255, 0)) 
            
            self.change_circle_color(QColor(0, 255, 0))  # 초록색으로 변경 
            self.statusbar.setStyleSheet('background-color: #00ff00; ')
            
            if self.ser and self.start_status:
                self.enable_st()
                self.img_box.setEnabled(False)
                self.experiment_input.setReadOnly(True)
                self.reward_input.setReadOnly(True)
                self.hav2_input.setReadOnly(True)
                self.touch_input.setReadOnly(True)
                self.ITI_input.setReadOnly(True)
                
                self.yes_btn.setEnabled(False)
                self.no_btn.setEnabled(False)
                time.sleep(0.1)
                self.start.setEnabled(False)
                time.sleep(0.1)
                self.start.setStyleSheet('')
                time.sleep(0.1)
                self.end.setEnabled(True)
                time.sleep(0.1)
                self.end.setStyleSheet('background-color: #d4cb51; ')
                time.sleep(0.1)
                self.receive_and_display_data()
                print(visual_select)
                
                
                
        else:
            print("Serial port is not open. Please open the port before starting the experiment.")




    def send_and_receive(self, command, data):
        desired_response = command
        found_response = False

        timeout = 10
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = self.ser.readline().decode('utf-8').strip()

            if desired_response in response:
                found_response = True
                break

        if found_response:
            print("응답이 도착했습니다:", response, data)
            self.ser.write(data + b'\n')
        else:
            print(response)
            print("응답을 찾지 못했습니다. 타임아웃")
            self.end_btn_()
            

    def receive_and_display_data(self):
        
        must_touch_trials = self.touch_input.text()
        
        
        
        
        if self.ser is not None:
            print(self.ser)
            buffer = ""
            
            while not self.stop_receiving_data:
                self.statusbar.showMessage("Start of the experiment")
                time.sleep(0.01)
                tempTime = time.time()
                data_received = self.ser.read(1024).decode('utf-8')
                # QApplication.processEvents()
                if data_received:
                    # QApplication.processEvents()
                    buffer += data_received

                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)

                        ###########################실험 끝나면 자동으로 종료###########################

                        if 'trial' in line and 'starts' in line:
                            trial_starts_parts = line.split(' ')
                            for part in trial_starts_parts:
                                if part.isdigit():
                                    self.trial_starts_value = int(part)
  
                                    break

                        if int(must_touch_trials) == self.trial_starts_value:
                            if 'trial done' in line:
                                        self.trial_done_detected = True

                        if int(must_touch_trials) == self.trial_starts_value and self.trial_done_detected:
                            self.trial_done_detected = False
                            QTimer.singleShot(10, self.end_btn_)  # QTimer를 사용하여 10ms 후에 end_btn_ 호출

                        ##############################################################################
                    
                        if line and line[0] == '*':  # video record 찾기
                            new_text = line[1:]
                            new_text = new_text.strip()
                            self.video_text.clear()  # 기존 텍스트를 모두 제거
                            self.video_text.insertPlainText(new_text)
                            # QApplication.processEvents()
                            
                        elif line and line[0] == '@':  # ITI 찾기
                            ITI_new_text = line[1:]
                            ITI_new_text = ITI_new_text.strip()
                            self.ITI_text.clear()  # 기존 텍스트를 모두 제거
                            self.ITI_text.insertPlainText(ITI_new_text)
                            # QApplication.processEvents()
                            if ITI_new_text:
                                if float(ITI_new_text[10:]) > float(self.ITI_input.text()) - 0.5:
                                    self.ITI_text.clear()
                                    
                        
                                    
                        elif line:
                            if line.startswith(self.img_box.currentText()):
                            # 조건에 해당하는 경우 라인을 출력하지 않고 넘어감
                                print(f"이거는 나오면 안되는거 : {line}")
                            else:
                                # 그 외의 경우에는 라인을 출력
                                self.text.insertPlainText(line)
                                print(f"Line doesn't start with '*' or '@': {line}")
                                scrollbar = self.text.verticalScrollBar()
                                scrollbar.setValue(scrollbar.maximum())
                                # QApplication.processEvents()
                                
                QApplication.processEvents()
        else:
            print("Serial port is not open. Please open the port before starting the data display.")


        
    def end_btn_(self):
        
        self.statusbar.setStyleSheet('background-color: #ff0000; ')
        
        self.change_circle_color(QColor(255, 0, 0))  # 빨강으로 변경
        self.img_change_circle_color(QColor(0, 0, 0))  
        self.experiment_change_circle_color(QColor(0, 0, 0))  
        self.reward_change_circle_color(QColor(0, 0, 0))  
        self.hav2_change_circle_color(QColor(0, 0, 0))  
        self.touch_change_circle_color(QColor(0, 0, 0))  
        self.ITI_change_circle_color(QColor(0, 0, 0))  
        self.video_change_circle_color(QColor(0, 0, 0)) 
        must_touch_trials = self.touch_input.text()
        
        
        print(f'must_touch_trials : {type(must_touch_trials)}, trial_done_detected : {self.trial_done_detected}, trial_starts_value : {type(self.trial_starts_value)}')
        
        self.statusbar.showMessage("Ready to connect")
        self.port_done.setText("연결")
        self.btn.setEnabled(True)
        self.port_done.setEnabled(True)
        
        
        
         # video 버튼 체크 해제
        # if self.yes_btn.isChecked():
        #     self.yes_btn.toggle()
        # if self.no_btn.isChecked():
        #     self.no_btn.toggle()
            
        
        
        
        self.ITI_text.clear()
        
        self.experiment_input.clear()
        # self.reward_input.clear()
        # self.hav2_input.clear()
        # self.touch_input.clear()
        # self.video_text.clear()
        # self.ITI_input.clear()
        
        self.port_done.setStyleSheet('background-color: #d4cb51; ')
        
        
        # self.img_box.clear()
        self.img_box.setEnabled(False)
        self.experiment_input.setReadOnly(True)
        self.reward_input.setReadOnly(True)
        self.hav2_input.setReadOnly(True)
        self.touch_input.setReadOnly(True)
        self.ITI_input.setReadOnly(True)
        
        self.yes_btn.setEnabled(False)
        self.no_btn.setEnabled(False)
        
        
      
        
    
        

        if self.ser:
            
            
            self.end.setEnabled(False)
            time.sleep(0.1)
            self.end.setStyleSheet('')
            
            self.stop_receiving_data = True
            
            self.video_text.clear()
            QApplication.processEvents()
            
            
            
            if self.ser:
                self.ser.write(ctrl_c)
                # self.ser.close()
                
                
                
                # self.ser = None
                time.sleep(0.5)
                self.run()
        # QTimer.singleShot(5000, self.port_done_btn) 
            # if self.restart and not self.ser:
                # QTimer.singleShot(500, self.port_done_btn)
                # self.port_done_btn()
                # self.restart = False
        
                     
            
            
    def pi_login(self):
        
            self.ser.write(b'\n')  # 엔터키 입력
            time.sleep(0.1)
            self.ser.write(b'pi\n')  # 사용자 이름 입력
            time.sleep(0.1)
            self.ser.write(b'password\n')  # 비밀번호 입력
            time.sleep(0.1)
            
            
            
        
     
    def run(self):
        
        
        self.statusbar.setStyleSheet('background-color: #ff9900; ')
        
        self.img_select()
        time.sleep(0.1)
        
        self.ser.write(b'cd Desktop\n')
        time.sleep(0.1)
        self.ser.write(b'export DISPLAY=:0\n')
        time.sleep(0.1)
        self.ser.write(b'python pretraining.py \n')
        time.sleep(0.1)
        
        desired_response = "Hello from the pygame community. https://www.pygame.org/contribute.html"
            # 이 문자열이 날라와야해서 변수에 저장
            
        found_response = False

        timeout = 3
        start_time = time.time()

        while time.time() - start_time < timeout:
            
            response = self.ser.readline().decode('utf-8').strip()

            if desired_response in response: # 여기서 문자열 올 때 까지 기다림
                found_response = True
                self.port_done.setText("연결 완료")
                break

        if found_response:
            print("응답이 도착했습니다:", response)
        else:
            print("응답을 찾지 못했습니다. 타임아웃")
            
        self.reset_style()   
            
        self.img_box.setEnabled(True)
        self.experiment_input.setReadOnly(False)
        self.reward_input.setReadOnly(False)
        self.hav2_input.setReadOnly(False)
        self.touch_input.setReadOnly(False)
        self.ITI_input.setReadOnly(False)
        
        self.yes_btn.setEnabled(True)
        self.no_btn.setEnabled(True)
        self.btn.setEnabled(False)
        self.port_done.setEnabled(False)
        self.port_list.setEnabled(False)
        self.port_done.setStyleSheet('')
        self.change_circle_color(QColor(255, 153, 0))  # 주황으로 변경     
            
        self.start.setEnabled(True)
        self.start.setStyleSheet('background-color: #d4cb51; ')
        self.statusbar.showMessage("Connected")   # 상태바 Connected 표시 
     
        
    def USB(self): # USB 연결 확인
        self.ser.write(b'ls /media/pi\n')  # ls 명령어로 디렉토리 확인
        time.sleep(0.1)

        ls_data = self.ser.read(1024).decode('utf-8')  # 실행 결과를 읽습니다.
        
        if self.USB_name in ls_data: # USB 이름이 있는지 연결확인
            return True
        else:
            return False
    
    def exit_btn(self):  # 라즈베리파이 종료 및 프로그램 종료
        # Create a message box with Yes and No buttons
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Message')
        msg_box.setText('실험장비도 종료 하시겠습니까?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Remove the default button
        msg_box.setDefaultButton(QMessageBox.No)

        # Connect the finished signal to a custom slot
        msg_box.finished.connect(self.handle_message_box_finish)

        # Show the message box
        msg_box.exec_()

    def handle_message_box_finish(self, result):
        # Process the user's choice
        if result == QMessageBox.Yes:
            try:
                if self.ser:  # 시리얼 포트 열려있으면 실행
                    if self.ser.is_open:
                        self.ser.write(ctrl_c)
                        time.sleep(0.1)
                        self.ser.write(b'sudo shutdown -h now\n')
                        time.sleep(0.1)
                        end_read = self.ser.read(1024).decode('utf-8')
                        print(end_read)
                        self.ser.close()  # 시리얼 포트를 닫습니다.
                        
                else: # 안열려 있으면 실행
                    try:
                        self.ser = serial.Serial(self.port_list.currentText(), 115200, timeout=1, stopbits=serial.STOPBITS_ONE)
                        time.sleep(0.1)
                        self.ser.write(b'\n')  # 엔터키 입력
                        time.sleep(0.1)
                        self.ser.write(b'pi\n')  # 사용자 이름 입력
                        time.sleep(0.1)
                        self.ser.write(b'password\n')  # 비밀번호 입력
                        time.sleep(0.5)
                        self.ser.write(ctrl_c)
                        time.sleep(0.5)
                        self.ser.write(b'sudo shutdown -h now\n')  
                        time.sleep(0.1)
                        end_read = self.ser.read(1024).decode('utf-8')
                        print(end_read)
                        self.close()
                        
                    except Exception as e:
                        print(f"An error occurred: {e}")
                QApplication.instance().quit()  # PyQt5 애플리케이션을 종료합니다.
            except Exception as e:
                print(f"An error occurred: {e}")
        elif result == QMessageBox.No:
            print("User closed the message box without selecting Yes.")
            self.close()
            # "No" 버튼을 눌렀을 때 추가로 수행할 동작을 여기에 추가
        else:
            print("User closed the message box without selecting Yes or No.")
            # Yes와 No 중 어느 버튼도 선택되지 않았을 때 추가로 수행할 동작을 여기에 추가
            pass
    

    

    def button_Second(self):
        self.hide()
        self.second = SecondWindowClass(self)
        self.second.exec()
        self.show()
        
        
        
    def toggle_radio_buttons(self):
            sender = self.sender()  # 시그널을 트리거한 버튼을 얻습니다.

            if sender == self.yes_btn:
                if self.yes_btn.isChecked():
                    self.no_btn.setChecked(False)
                
            elif sender == self.no_btn:
                if self.no_btn.isChecked():
                    self.yes_btn.setChecked(False)
                
                
    def data_clear(self):
        self.text.clear()
        self.video_text.clear()





    def save_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save to Notepad", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_path:
            # Ensure that the file path has the ".txt" extension
            if not file_path.endswith(".txt"):
                file_path += ".txt"

            text_content = self.text.text()
            try:
                with open(file_path, 'w') as file:
                    file.write(text_content)
                QMessageBox.information(self, 'Success', f'Text saved to {file_path}')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')



    def img_select(self):
        self.ser.write(f'ls /media/pi/{self.USB_name}/visuals\n'.encode('utf-8'))  
        time.sleep(0.1)
        img_read = self.ser.read(1024).decode('utf-8')
        time.sleep(0.1)

        # 파일 목록 중 .png 확장자를 가진 파일만 추출
        file_list = [file.strip() for file in img_read.split() if file.endswith('.png')]

        # 기존 목록 가져오기
        current_items = [self.img_box.itemText(i) for i in range(self.img_box.count())]

        # 새로 추가할 항목 찾기
        new_items = [file for file in file_list if file not in current_items]

        # combo box에 새로운 항목 추가
        self.img_box.addItems(new_items)

        time.sleep(0.1)

        # self.img_status = True
        

    def is_numeric(self,text):
        try:
            float_value = float(text)
            return True
        except ValueError:
            return False

    
    # def Disconnecting(self):
    #     if self.ser:
    #         self.ser.write(ctrl_c)
    #         self.ser.close()
            
            
            
    #         self.ser = None

    def enable_st(self):
        self.experiment_input.setStyleSheet('background-color: #cccaca; border: 1px solid #cccccc; ')
        self.reward_input.setStyleSheet('background-color: #cccaca; border: 1px solid #cccccc; ')
        self.hav2_input.setStyleSheet('background-color: #cccaca; border: 1px solid #cccccc; ')
        self.touch_input.setStyleSheet('background-color: #cccaca; border: 1px solid #cccccc; ')
        self.ITI_input.setStyleSheet('background-color: #cccaca; border: 1px solid #cccccc; ') 




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
