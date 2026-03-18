from PyQt5 import QtWidgets, QtCore
import sys
from datetime import datetime

class CountdownWidget(QtWidgets.QWidget):
    def __init__(self, target_hour, target_minute):
        super().__init__()

        # 레이아웃 생성 (여백 0)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 레이블
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size:65px;
            font-family:Consolas;
            background-color:white;
            color:black;
        """)
        layout.addWidget(self.label)

        # 타이머
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # 목표 시간
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.set_target_time()
        self.update_timer()

        # 위젯 크기 딱 맞춤
        self.adjustSize()

    def set_target_time(self):
        now = datetime.now()
        self.target_time = now.replace(
            hour=self.target_hour,
            minute=self.target_minute,
            second=0,
            microsecond=0
        )
        if self.target_time < now:
            self.target_time = now

    def update_timer(self):
        now = datetime.now()
        remaining = self.target_time - now

        if remaining.total_seconds() > 0:
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.label.setText("00:00:00")

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("수업 타이머")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)

        # 탭 생성
        lunch_tab = CountdownWidget(13, 20)   # 점심시간
        end_tab = CountdownWidget(18, 20)     # 수업종료

        self.tabs.addTab(lunch_tab, "점심시간")
        self.tabs.addTab(end_tab, "수업종료")

        layout.addWidget(self.tabs)

        # 창 크기 딱 맞춤 + 고정
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

        # 우측 하단 배치
        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = screen_geometry.right() - self.width() - 5
        y = screen_geometry.bottom() - self.height() - 34
        self.move(x, y)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())