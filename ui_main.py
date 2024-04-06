import sys
from PyQt5.QtWidgets import *
import subprocess
import os
import multiprocessing as multi
from ui_widget import Ui_Form
from ui_pager import ImagePager
from stylesheet import stylesheet


class CustomWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.toolButton_objfile.clicked.connect(self.openFileDialog)
        self.toolButton_texturedir.clicked.connect(self.openDirectoryDialog)
        self.toolButton_output.clicked.connect(self.openDirectoryDialog)

    # 선택된 파일의 경로를 반환합니다.
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "파일 선택", "")
        if fileName:
            self.lineEdit_objfile.setText(fileName)  # lineEdit에 파일 경로를 설정합니다.

    # 선택된 디렉토리의 경로를 반환합니다.
    def openDirectoryDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "디렉토리 선택", "")
        if directory:
            # sender()를 사용하여 어떤 버튼이 클릭되었는지 확인하고, 해당하는 lineEdit에 경로를 설정합니다.
            if self.sender() == self.toolButton_texturedir:
                self.lineEdit_texturedir.setText(directory)
            elif self.sender() == self.toolButton_output:
                self.lineEdit_output.setText(directory)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.gridLayout = QGridLayout()

        # controlsLayout = spinBox + generateButton
        self.controlsLayout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.controlsLayout.addSpacerItem(spacer)
        self.spinBox = QSpinBox(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(12)
        self.spinBox.setValue(3)  # 기본으로 생성되는 위젯의 개수가 됌
        self.controlsLayout.addWidget(self.spinBox)
        self.generateButton = QPushButton("Generate Widgets", self)
        self.controlsLayout.addWidget(self.generateButton)
        self.generateButton.clicked.connect(self.generateWidgets)

        # mainLayout = controlsLayout + gridLayout
        self.mainLayout.addLayout(self.controlsLayout)  # 컨트롤 레이아웃을 메인 레이아웃에 추가
        self.mainLayout.addLayout(self.gridLayout)  # 격자 레이아웃을 메인 레이아웃에 추가

        # startAllLayout = leftSpacer + startAllLayout + rightSpacer
        self.startAllLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.startAllLayout.addSpacerItem(leftSpacer)
        self.startAllButton = QPushButton("Start All", self)
        self.startAllLayout.addWidget(self.startAllButton)
        rightSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.startAllLayout.addSpacerItem(rightSpacer)

        # mainLayout = controlsLayout + gridLayout + startAllLayout
        self.mainLayout.addLayout(self.startAllLayout)

        self.widgets = []
        self.outputframepath = []
        self.generateWidgets()  # 초기 위젯 생성
        self.startAllButton.clicked.connect(self.startAll)

    # spinbox의 value만큼 위젯 생성
    def generateWidgets(self):
        self.clearWidgets()  # 기존 위젯 제거
        for i in range(self.spinBox.value()):
            widget = CustomWidget(self)
            widget.setMinimumSize(400, 120)
            self.gridLayout.addWidget(widget, int(i // 3), int(i % 3))  # 위젯을 3x3 격자 레이아웃으로 생성
            self.widgets.append(widget)

    def clearWidgets(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.widgets.clear()

    # 멀티 프로세스로 모든 위젯에 대해 병렬 처리합니다 (이렇게 해서 모든 파일(위젯)이 동시에 렌더되도록 하였습니다)
    def startAll(self):
        processes = []
        for widget in self.widgets:
            objfile = widget.lineEdit_objfile.text()
            texture = widget.lineEdit_texturedir.text()
            output = widget.lineEdit_output.text()
            framepath = os.path.join(output, "frame_0001.png")
            self.outputframepath.append(framepath)
            print("------------------------------", self.outputframepath)

            p = multi.Process(target=self.run_main_py, args=(objfile, texture, output))  # 병렬 처리 프로세스 생성
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        reply = QMessageBox.question(
            self, "작업 완료", "모든 작업이 완료되었습니다. 결과를 확인하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        # yes를 선택하면, 작업이 끝난 결과물을(1프레임만) 한 장씩 보여줍니다.
        if reply == QMessageBox.Yes:
            last_output_dir = self.outputframepath
            self.imagepager = ImagePager(last_output_dir)
            self.imagepager.resize(1920, 980)
            self.imagepager.show()

    @staticmethod
    def run_main_py(objfile, texture, output):
        # 사용자의 홈 디렉토리를 참조하도록 설정합니다.
        home_directory = os.path.expanduser("~")

        # main.py 스크립트의 경로를 동적으로 설정합니다.
        script_path = os.path.join(home_directory, "myproject", "main.py")

        # 외부 명령(mayapy를 사용한 스크립트)을 실행합니다.
        subprocess.run(["/usr/autodesk/maya2024/bin/mayapy", script_path, objfile, texture, output], check=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec())
