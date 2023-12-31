import sys                              
from PyQt5.QtWidgets import *           # PyQt5 사용하기 위한 것
from PyQt5 import uic                   # ui 파일을 직접 이용하기 위한 것
from PyQt5.QtGui import *
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
        self.setWindowTitle("Operant_Chamber_Ver 1.0")
        self.setWindowIcon(QIcon("Scitech_Korea.png"))
        
        self.btn1_clicked()
        
        
        self.btn.clicked.connect(lambda: (self.btn_clicked(), self.btn1_clicked()))
        self.port_done.clicked.connect(self.port_done_btn)
        self.start.clicked.connect(self.start_btn_)
        self.end.clicked.connect(self.end_btn_)
        
        self.ser = None
        self.stop_receiving_data = False

    def btn_clicked(self):
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
        try:
            ser = serial.Serial(self.port_list.currentText(), 115200,timeout=1, stopbits=serial.STOPBITS_ONE)
            self.ser = ser
            print("성공")
            
            self.run()
            
            desired_response = "Hello from the pygame community. https://www.pygame.org/contribute.html"
            # 이 문자열이 날라와야해서 변수에 저장
            found_response = False

            timeout = 3
            start_time = time.time()

            while time.time() - start_time < timeout:
                
                response = ser.readline().decode('utf-8').strip()
    
                if desired_response in response: # 여기서 문자열 올 때 까지 기다림
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
        if self.ser:
            self.stop_receiving_data = False
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
    
            self.text.insertPlainText('experiment_id :' + experiment_id.decode('utf-8') + '\n')
            self.text.insertPlainText('reward duration :' + rd.decode('utf-8') + '\n')
            self.text.insertPlainText('habv2 trials :' + habv2_trials.decode('utf-8') + '\n')
            self.text.insertPlainText('must touch trials :' + must_touch_trials.decode('utf-8') + '\n')
            self.text.insertPlainText('video recording :' + video.decode('utf-8') + '\n')
    
            self.send_and_receive("experiment id:", experiment_id)
            self.send_and_receive("reward duration:", rd)
            self.send_and_receive("habv2 trials:", habv2_trials)
            self.send_and_receive("must touch trials:", must_touch_trials)
            self.send_and_receive("video recording?(y/n):", video)

            if self.ser:
                self.receive_and_display_data()
                
            else:
                print("Serial port is not open. Please open the port before starting the experiment.")
        
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
            print("응답을 찾지 못했습니다. 타임아웃")

    def receive_and_display_data(self):
        
        if self.ser is not None:
            print(self.ser)
            buffer = ""  # 데이터를 저장할 버퍼 변수

        while not self.stop_receiving_data:
            time.sleep(0.01)
            tempTime = time.time()
            data_received = self.ser.read(1024).decode('utf-8')  # 데이터를 읽습니다 (예: 1024바이트 읽음)

            if data_received:
                buffer += data_received  # 읽은 데이터를 버퍼에 추가

                # 데이터를 한 줄씩 처리
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    
                    if line and line[0] == '*':  # video record 찾기
                        new_text = line[1:]
                        self.video_text.clear()  # 기존 텍스트를 모두 제거
                        self.video_text.insertPlainText(new_text)
                        QApplication.processEvents()
                        
                    elif line and line[0] == '@':  # ITI 찾기
                        ITI_new_text = line[1:]
                        self.ITI_text.clear()  # 기존 텍스트를 모두 제거
                        self.ITI_text.insertPlainText(ITI_new_text)
                        QApplication.processEvents()
                        if line and float(ITI_new_text[10:]) > 19.5:
                            self.ITI_text.clear()
                        
                    elif line:
                        self.text.insertPlainText(line)
                        print(f"Line doesn't start with '*' or '@': {line}")
                        QApplication.processEvents()
        else:
            print("Serial port is not open. Please open the port before starting the data display.")


        
    def end_btn_(self):
        self.video_text.clear()
        self.ITI_text.clear()
        self.text.clear()
        self.experiment_input.clear()
        self.reward_input.clear()
        self.hav2_input.clear()
        self.touch_input.clear()
        self.video_text.clear()
        
        if self.yes_btn.isChecked() == True:
            self.yes_btn.toggle()
        elif self.no_btn.isChecked() == True:
            self.no_btn.toggle()
        
        
    
        ctrl_c = b'\x03'

        if self.ser:
            
            
            self.stop_receiving_data = True
            
            self.ser.write(ctrl_c)
            self.ser.close()
            
            
    def run(self):
        
            self.ser.write(b'\n')  # 엔터키 입력
            time.sleep(1)
            self.ser.write(b'pi\n')  # 사용자 이름 입력
            time.sleep(1)
            self.ser.write(b'password\n')  # 비밀번호 입력
            time.sleep(1)
            self.ser.write(b'cd Desktop\n')
            time.sleep(1)
            self.ser.write(b'export DISPLAY=:0\n')
            time.sleep(1)
            self.ser.write(b'python pretraining.py \n')
            time.sleep(1)
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
