import sys                              
from PyQt5.QtWidgets import *           # PyQt5 사용하기 위한 것
from PyQt5 import uic                   # ui 파일을 직접 이용하기 위한 것
from PyQt5.QtGui import *
import serial.tools.list_ports
import time
import os
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout
import subprocess
import pickle
import numpy

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import pickle

form_secondwindow = uic.loadUiType("secondwindow.ui")[0]  # 두 번째창 ui

class secondwindow(QDialog, form_secondwindow):
    def __init__(self, parent=None):
        super(secondwindow, self).__init__()
        self.initUI()
        self.show()  # 두번째창 실행
        self.setWindowTitle("Operant_Chamber_Ver 1.0")
        self.setWindowIcon(QIcon("Scitech_Korea.png"))

    def initUI(self):
        self.setupUi(self)
        self.home_btn.clicked.connect(self.Home)
        self.serch_btn.clicked.connect(self.open_file_dialog)
        self.clear_btn.clicked.connect(self.clear)

        # QTableWidget 초기화
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(10, 10, 300, 400)

    def Home(self):
        self.close()  # 창 닫기

    def is_numeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def open_file_dialog(self):  # .pkl파일 열어서 데이터 확인하는 함수
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "Pickle Files (*.pkl);;All Files (*)",
                                                   options=options)

        if file_name:
            # 피클 파일 열기
            with open(file_name, 'rb') as file:
                try:
                    # pickle 파일 열기
                    data = pickle.load(file)

                    # 데이터를 QTableWidget에 삽입
                    self.table_widget.clearContents()
                    self.table_widget.setRowCount(len(data) * 2)  # 각 딕셔너리 키마다 2개의 행 필요
                    self.table_widget.setColumnCount(2)

                    row = 0
                    for key, value in data.items():
                        # 'out_poke' 키를 처음 만났을 때는 값을 추가하지 않음
                        if key == 'out_poke' and isinstance(value, dict):
                            for inner_key, inner_value in value.items():
                                inner_key_item = QTableWidgetItem(f"{key} - {inner_key}")
                                inner_value_str = str(inner_value)
                                # '['로 시작하거나 ']'로 끝나는 경우 제거
                                inner_value_str = inner_value_str.strip('[]')
                                inner_value_items = inner_value_str.split(",")  # 쉼표를 기준으로 나눠서 리스트로 변환
                                for idx, item in enumerate(inner_value_items):
                                    item_item = QTableWidgetItem(item.strip())  # 좌우 공백 제거
                                    # 유닉스 타임스탬프인 경우에만 변환 적용
                                    if self.is_numeric(item.strip()):
                                        timestamp = float(item.strip())
                                        if timestamp >= 1500000000:
                                            # timestamp += 9 * 3600  # Add 9 hours
                                            converted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                                            item_item = QTableWidgetItem(converted_time)
                                    self.table_widget.setItem(row + idx, 0, inner_key_item)
                                    self.table_widget.setItem(row + idx, 1, item_item)

                                row += len(inner_value_items)
                        else:
                            key_item = QTableWidgetItem(str(key))
                            value_str = str(value)
                            # '['로 시작하거나 ']'로 끝나는 경우 제거
                            value_str = value_str.strip('[]')
                            value_items = value_str.split(",")  # 쉼표를 기준으로 나눠서 리스트로 변환
                            for idx, item in enumerate(value_items):
                                item_item = QTableWidgetItem(item.strip())  # 좌우 공백 제거
                                # 유닉스 타임스탬프인 경우에만 변환 적용
                                if self.is_numeric(item.strip()):
                                    timestamp = float(item.strip())
                                    if timestamp >= 1600000000:
                                        # timestamp += 9 * 3600  # Add 9 hours
                                        converted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                                        item_item = QTableWidgetItem(converted_time)
                                self.table_widget.setItem(row + idx, 0, key_item)
                                self.table_widget.setItem(row + idx, 1, item_item)

                            row += len(value_items)

                    # 각 열의 크기 조절
                    self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                    self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

                except Exception as e:
                    # 예외 처리: 피클 파일이 올바르게 열리지 않은 경우
                    print(f"피클 파일 로딩 중 오류 발생: {e}")

    def clear(self):
        self.table_widget.clearContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = secondwindow()
    myWindow.show()
    app.exec_()