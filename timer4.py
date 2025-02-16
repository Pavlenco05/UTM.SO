import time
import random
import threading

class Timer4:
    def __init__(self, update_callback):
        self.time = 10 * 60  # 10 минут для основного времени
        self.running = False
        self.update_callback = update_callback
        self.penalty_time = 0
        self.timeout = False
        self.break_time = False

    def start(self):
        self.running = True
        self.timeout = False
        self.break_time = False
        self._countdown()

    def stop(self):
        self.running = False

    def _countdown(self):
        while self.running and self.time > 0:
            if self.timeout or self.break_time:
                time.sleep(1)
                continue
            time.sleep(1)
            self.time -= 1
            self.update_callback(self.time)

        if self.running:
            self._random_event()

    def add_time(self, minutes):
        self.time += minutes * 60  # добавление времени в минутах
        self.update_callback(self.time)

    def add_penalty(self):
        self.time += 2 * 60  # добавление 2 минут на штраф
        self.update_callback(self.time)

    def start_timeout(self):
        self.timeout = True
        self.update_callback("Таймаут! Время остановлено.")

    def end_timeout(self):
        self.timeout = False
        self.update_callback("Таймаут завершен.")

    def start_break(self):
        self.break_time = True
        self.update_callback("Перерыв! Время остановлено.")

    def end_break(self):
        self.break_time = False
        self.update_callback("Перерыв завершен.")

    def _random_event(self):
        event_time = random.randint(0, self.time)
        self.update_callback(f"Событие! Время: {event_time//60} мин")
