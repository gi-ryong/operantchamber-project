import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pickle

form_secondwindow = uic.loadUiType("secondwindow.ui")[0] #두 번째창 ui
class secondwindow(QDialog, QWidget,form_secondwindow):
    def __init__(self, parent=None):
        super(secondwindow,self).__init__()
        self.initUI()
        self.show() # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.home_btn.clicked.connect(self.Home)
        self.serch_btn.clicked.connect(self.open_file_dialog)
        self.clear_btn.clicked.connect(self.clear)
        
    def Home(self):
        self.close() #창 닫기
           
        
    def open_file_dialog(self):   #.pkl파일 열어서 데이터 확인하는 함수
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "Pickle Files (*.pkl);;All Files (*)", options=options)

        if file_name:
            # 피클 파일 열기
            with open(file_name, 'rb') as file:
                try:
                    # pickle 파일 열기
                    data = pickle.load(file)

                    # 데이터를 문자열로 변환하여 QTextEdit에 삽입
                    data_str = str(data)
                    self.data_text.clear()  # 기존 내용 지우기
                    self.data_text.insertPlainText(data_str)
                except Exception as e:
                    # 예외 처리: 피클 파일이 올바르게 열리지 않은 경우
                    print(f"Error loading pickle file: {e}")
                    
                    
                    
    def clear(self):
        self.data_text.clear()