import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class GameTimer:
    def __init__(self, callback, duration_minutes=20):
        self.callback = callback
        self.duration = duration_minutes * 60  
        self.current_time = self.duration
        self.is_running = False
        self.is_timeout = False
        self.is_break = False
        
    def start(self):
        self.is_running = True
        
    def stop(self):
        self.is_running = False
        
    def update_time(self):
        if self.is_running and not self.is_timeout and not self.is_break:
            if self.current_time > 0:
                self.current_time -= 1
                self.callback(self.current_time)
            else:
                self.stop()
                self.callback("Период завершен")
                
    def add_time(self, minutes):
        self.current_time += minutes * 60
        self.callback(self.current_time)
        
    def add_penalty(self):
        # Add 2 minute penalty
        self.current_time += 120
        self.callback(self.current_time)
        
    def start_timeout(self):
        self.is_timeout = True
        self.callback("Таймаут")
        
    def end_timeout(self):
        self.is_timeout = False
        self.callback(self.current_time)
        
    def start_break(self):
        self.is_break = True
        self.callback("Перерыв")
        
    def end_break(self):
        self.is_break = False
        self.callback(self.current_time)

class HockeyGameApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Хоккейный Таймер")
        self.setGeometry(100, 100, 300, 400)

        # Create timers for each period
        self.timer1 = GameTimer(self.update_time_display)
        self.timer2 = GameTimer(self.update_time_display)
        self.timer4 = GameTimer(self.update_time_display)
        
        self.current_timer = None

        # UI Setup
        self.time_label = QLabel("20:00", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px;")

        self.start_button = QPushButton("Старт", self)
        self.start_button.clicked.connect(self.start_timer1)

        self.penalty_button = QPushButton("Штраф +2 мин", self)
        self.penalty_button.clicked.connect(self.add_penalty)

        self.time_button = QPushButton("Добавить время", self)
        self.time_button.clicked.connect(self.add_time)

        self.timeout_button = QPushButton("Таймаут", self)
        self.timeout_button.clicked.connect(self.start_timeout)

        self.break_button = QPushButton("Перерыв", self)
        self.break_button.clicked.connect(self.start_break)

        self.status_label = QLabel("Готово к началу", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.penalty_button)
        layout.addWidget(self.time_button)
        layout.addWidget(self.timeout_button)
        layout.addWidget(self.break_button)
        layout.addWidget(self.status_label)

        # Update timer setup
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_game)
        self.update_timer.start(1000)  # Update every second

    def update_time_display(self, time):
        if isinstance(time, int):
            mins, secs = divmod(time, 60)
            self.time_label.setText(f"{mins:02d}:{secs:02d}")
        else:
            self.status_label.setText(time)

    def start_timer1(self):
        if self.current_timer:
            self.current_timer.stop()
        self.status_label.setText("Первый период начался")
        self.current_timer = self.timer1
        self.timer1.start()

        self.start_button.setText("Старт 2-й период")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_timer2)

    def start_timer2(self):
        if self.current_timer:
            self.current_timer.stop()
        self.status_label.setText("Второй период начался")
        self.current_timer = self.timer2
        self.timer2.start()

        self.start_button.setText("Старт 4-й период")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_timer4)

    def start_timer4(self):
        if self.current_timer:
            self.current_timer.stop()
        self.status_label.setText("Четвертый период начался")
        self.current_timer = self.timer4
        self.timer4.start()

        self.start_button.setText("Игра завершена")
        self.start_button.setEnabled(False)

    def update_game(self):
        if self.current_timer:
            self.current_timer.update_time()

    def add_time(self):
        if self.current_timer:
            self.current_timer.add_time(5)

    def add_penalty(self):
        if self.current_timer:
            self.current_timer.add_penalty()

    def start_timeout(self):
        if self.current_timer:
            self.current_timer.start_timeout()

    def start_break(self):
        if self.current_timer:
            self.current_timer.start_break()

    def closeEvent(self, event):
        if self.current_timer:
            self.current_timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HockeyGameApp()
    window.show()
    sys.exit(app.exec())