import sys                              
from PyQt5.QtWidgets import *           # PyQt5 사용하기 위한 것
from PyQt5 import uic                   # ui 파일을 직접 이용하기 위한 것.
import serial.tools.list_ports
import time
import os
import serial

form_class = uic.loadUiType("port.ui")[0]



nnum = 0                            # 여기에 선언하면 전역변수라는 

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
        global nnum                 # 이렇게 하면 전역 변수를 사용함.
        nnum =  nnum+1;
        # self.listWidget.addItem("Text add " + str(nnum))
        self.port_list.addItem("COM"+str(nnum))

    def btn1_clicked(self):
        self.port_list.clear()           # 찾기 버튼 두 번 이상 눌렀을 때 대비용
        ports = serial.tools.list_ports.comports()
        
        available_ports = []
        for p in ports:
            available_ports.append(p.device)    
        if len(available_ports) > 0:
            available_ports.sort()                  # 이 부분이 있어야..
            for  aa in available_ports:
                self.port_list.addItem(aa)
                
                
                
                
    def port_done_btn(self):
        try:
            ser = serial.Serial(self.port_list.currentText(), 115200, stopbits=serial.STOPBITS_ONE)
            self.ser = ser
            print("성공")
            ser.write(b'\n')  # 엔터키 입력
            time.sleep(1)  # 잠시 대기
            ser.write(b'pi\n')  # 사용자 이름 입력
            time.sleep(1)  # 잠시 대기
            ser.write(b'password\n')  # 비밀번호 입력
            time.sleep(1)  # 잠시 대기
            ser.write(b'cd Desktop\n')
            time.sleep(1)  # 잠시 대기
            ser.write(b'export DISPLAY=:0\n')
            time.sleep(1)  # 잠시 대기
            ser.write(b'python pretraining.py \n')
            time.sleep(1)  # 잠시 대기
            
            
            
            
            # 원하는 응답 패턴 설정
            desired_response = "Hello from the pygame community. https://www.pygame.org/contribute.html"
            found_response = False

            # 타임아웃 설정 (예: 10초)
            timeout = 10
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
                
                
                

        
            # 타임아웃 설정 (예: 5초)
            ser.timeout = 10
        
            
            output = ser.read_all()
            output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
            print(output_str)
            self.text.setPlainText(output_str)
            
            # ex_desired_response = "experiment id: "
            # ex_found_response = False

            #     # 타임아웃 설정 (예: 10초)
            # timeout = 10
            # start_time = time.time()
            # while time.time() - start_time < timeout:
            #     ex_response = self.ser.readline().decode('utf-8').strip()

            #     if ex_desired_response in ex_response:
            #         ex_found_response = True
            #         break
            # if ex_found_response:
            #     print("응답이 도착했습니다:", ex_response)
            # else:
            #     print("응답을 찾지 못했습니다. 타임아웃")
                
                
            # ser.timeout = 10
        
        # 여기에서 다른 작업을 수행
            # ser.close()  # 사용이 끝나면 시리얼 포트를 닫음
            
        except serial.SerialException as e:
            print(f"Failed to open the serial port: {e}")
            print(type(self.port_list.currentText()), self.port_list.currentText())


        
      
        
        
        
        
        
        
    # def start_btn_(self):
        
    #     if self.ser is not None and self.ser.is_open: 
    #         experiment_id = self.experiment_input.toPlainText()
    #         rd = self.reward_input.toPlainText()
    #         habv2_trials = self.hav2_input.toPlainText()
    #         must_touch_trials = self.touch_input.toPlainText()
    #         if self.yes_btn.isChecked():
    #             video = 'y'
    #         elif self.no_btn.isChecked():
    #             video = 'n'
                
              
    #         self.ser.write(experiment_id.encode('utf-8'))  # 엔터키 입력
    #         time.sleep(1)  # 잠시 대기
    #         self.ser.write(rd.encode('utf-8'))  # 엔터키 입력
    #         time.sleep(1)  # 잠시 대기
    #         self.ser.write(habv2_trials.encode('utf-8'))  # 엔터키 입력
    #         time.sleep(1)  # 잠시 대기
    #         self.ser.write(must_touch_trials.encode('utf-8'))  # 엔터키 입력
    #         time.sleep(1)  # 잠시 대기
    #         self.ser.write(video.encode('utf-8'))  # 엔터키 입력
    #         time.sleep(1)  # 잠시 대기
            
    
    
    
    
    
    
    
    
    def start_btn_(self):
        
        
        
        # if self.ser is not None and self.ser.is_open:
        
        
        experiment_id = self.experiment_input.toPlainText()
        rd = self.reward_input.toPlainText()
        habv2_trials = self.hav2_input.toPlainText()
        must_touch_trials = self.touch_input.toPlainText()
        if self.yes_btn.isChecked():
            video = 'y'
        elif self.no_btn.isChecked():
            video = 'n'
            
              
        
        self.text.insertPlainText(experiment_id +'\n')
        self.text.insertPlainText (rd +'\n')
        self.text.insertPlainText (habv2_trials +'\n')
        self.text.insertPlainText (must_touch_trials +'\n')
        self.text.insertPlainText (video +'\n')
        
        experiment_id = experiment_id.encode('utf-8')
        rd = rd.encode('utf-8')
        habv2_trials = habv2_trials.encode('utf-8')
        must_touch_trials = must_touch_trials.encode('utf-8')
        video = video.encode('utf-8')
        
        time.sleep(1)
    ##################################  
        
                
                
        self.ser.write(experiment_id)
        time.sleep(5)  # 잠시 대기
        
        
        
        
        
        self.ser.timeout = 10
        
            
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
        
    ################################## 
    
        
        
        self.ser.timeout = 10
        
            
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
        
        self.ser.write(rd)
        time.sleep(5)  # 잠시 대기
        
        self.ser.timeout = 10
        
            
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
                 
    ################################## 
    
        self.ser.write(habv2_trials)
        time.sleep(5)  # 잠시 대기
    
        self.ser.timeout = 10
        
            
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
        
    ##################################
    
        self.ser.write(must_touch_trials)
        time.sleep(5)  # 잠시 대기
        
        self.ser.timeout = 10
        
            
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
        
    ##################################
    
        self.ser.write(video)
        time.sleep(5)  # 잠시 대기
        
        self.ser.timeout = 10
    
        output = self.ser.read_all()
        output_str = output.decode('utf-8')  # bytes를 문자열로 디코딩
        print(output_str)
        self.text.setPlainText(output_str)
    
    ##################################
    
    
        
        
        
        
        
def send_and_receive(self, prompt, value):
    self.text.insertPlainText(prompt + ' ' + value + '\n')
    value = value.encode('utf-8')
    self.ser.write(value)
    
    # 라즈베리 파이 응답 처리
    response = self.ser.readline().decode('utf-8').strip()
    print(response)
    self.text.insertPlainText(response + '\n')
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()