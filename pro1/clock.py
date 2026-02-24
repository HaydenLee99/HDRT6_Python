from PyQt5 import QtWidgets, QtCore
import sys
from datetime import datetime

class CountdownTimer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("수업종료")

        # 타이머 레이블
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size:65px; background-color:white; color:black;")

        # 항상 위에 표시
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # PyQt 타이머: 1초마다 update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # 목표 시간: 오늘 18:20
        now = datetime.now()
        self.target_time = now.replace(hour=18, minute=20, second=0, microsecond=0)
        if self.target_time < now:
            self.target_time = now

        self.update_timer()

        # 라벨 크기에 맞게 창 크기 조정
        self.label.adjustSize()
        self.resize(self.label.width(), self.label.height())

        # 우측 하단에 위치시키기
        self.move_to_bottom_right()

    def update_timer(self):
        now = datetime.now()
        remaining = self.target_time - now
        if remaining.total_seconds() > 0:
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.label.setText("00:00:00")
            self.timer.stop()

        # 매번 텍스트 길이에 맞춰 창 크기 조정
        self.label.adjustSize()
        self.resize(self.label.width(), self.label.height())
        # 위치도 다시 조정
        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # 작업 표시줄 제외 영역
        x = screen_geometry.right() - self.width() - 5  # 오른쪽에서 20px 여유
        y = screen_geometry.bottom() - self.height() - 34 # 아래쪽에서 20px 여유
        self.move(x, y)

app = QtWidgets.QApplication(sys.argv)
window = CountdownTimer()
window.show()
sys.exit(app.exec_())
