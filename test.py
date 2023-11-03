import sys                              
from PyQt5.QtWidgets import *           # PyQt5 사용하기 위한 것
from PyQt5 import uic                   # ui 파일을 직접 이용하기 위한 것
import serial.tools.list_ports
import time
import os
import serial

form_class = uic.loadUiType("port.ui")[0]

nnum = 0  # 여기에 선언하면 전역변수

class WindowClass(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn.clicked.connect(self.btn_clicked)
        self.btn.clicked.connect(self.btn1_clicked)
        self.port_done.clicked.connect(self.port_done_btn)
        self.start.clicked.connect(self.start_btn_)
        
        self.ser = None

    def btn_clicked(self):
        global nnum
        nnum = nnum + 1
        self.port_list.addItem("COM" + str(nnum))

    def btn1_clicked(self):
        self.port_list.clear()
        ports = serial.tools.list_ports.comports()
        
        available_ports = []
        for p in ports:
            available_ports.append(p.device)    
        if len(available_ports) > 0:
            available_ports.sort()
            for aa in available_ports:
                self.port_list.addItem(aa)
                
    def port_done_btn(self):
        try:
            ser = serial.Serial(self.port_list.currentText(), 115200,timeout=1, stopbits=serial.STOPBITS_ONE)
            self.ser = ser
            print("성공")
            ser.write(b'\n')  # 엔터키 입력
            time.sleep(1)
            ser.write(b'pi\n')  # 사용자 이름 입력
            time.sleep(1)
            ser.write(b'password\n')  # 비밀번호 입력
            time.sleep(1)
            ser.write(b'cd Desktop\n')
            time.sleep(1)
            ser.write(b'export DISPLAY=:0\n')
            time.sleep(1)
            ser.write(b'python pretraining.py \n')
            time.sleep(1)
            
            desired_response = "Hello from the pygame community. https://www.pygame.org/contribute.html"
            found_response = False

            timeout = 3
            start_time = time.time()

            while time.time() - start_time < timeout:
                
                response = ser.readline().decode('utf-8').strip()
    
                if desired_response in response:
                    found_response = True
                    break

            if found_response:
                print("응답이 도착했습니다:", response)
            else:
                print("응답을 찾지 못했습니다. 타임아웃")
                
        except serial.SerialException as e:
            print(f"Failed to open the serial port: {e}")
            print(type(self.port_list.currentText()), self.port_list.currentText())

    def start_btn_(self):
        experiment_id = self.experiment_input.toPlainText()
        rd = self.reward_input.toPlainText()
        habv2_trials = self.hav2_input.toPlainText()
        must_touch_trials = self.touch_input.toPlainText()
        if self.yes_btn.isChecked():
            video = 'y'
        elif self.no_btn.isChecked():
            video = 'n'
            
        experiment_id = experiment_id.encode('utf-8')
        rd = rd.encode('utf-8')
        habv2_trials = habv2_trials.encode('utf-8')
        must_touch_trials = must_touch_trials.encode('utf-8')
        video = video.encode('utf-8')

        self.text.insertPlainText(experiment_id.decode('utf-8') +'\n')
        self.text.insertPlainText(rd.decode('utf-8') +'\n')
        self.text.insertPlainText(habv2_trials.decode('utf-8') +'\n')
        self.text.insertPlainText(must_touch_trials.decode('utf-8') +'\n')
        self.text.insertPlainText(video.decode('utf-8') +'\n')

        self.send_and_receive("experiment id:", experiment_id)
        self.send_and_receive("reward duration:", rd)
        self.send_and_receive("habv2 trials:", habv2_trials)
        self.send_and_receive("must touch trials:", must_touch_trials)
        self.send_and_receive("video recording?(y/n):", video)
        
        
        
        self.receive_and_display_data()

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
            print("응답이 도착했습니다:", response)
            self.ser.write(data + b'\n')
        else:
            print("응답을 찾지 못했습니다. 타임아웃")

    def receive_and_display_data(self):
        
        video_text_check = ''
        
        while True:
            time.sleep(0.01)
            
            tempTime = time.time()
            
            #response = self.ser.readline().decode('utf-8').strip()
            while True:
                #self.text.append(response)  # append 메서드를 사용하여 다음 줄에 추가
                response = self.ser.readline().decode('utf-8').strip()
                print(response)
                if not response:
                    break
                
            #self.text.insertPlainText(response)  # append 메서드를 사용하여 다음 줄에 추가
            #QApplication.processEvents()
            print(time.time() - tempTime)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
