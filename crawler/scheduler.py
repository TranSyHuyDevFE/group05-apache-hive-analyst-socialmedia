import threading
import time

class HourlyScheduler:
    def __init__(self, func):
        self.func = func
        self._timer = None
        self._running = False

    def _run(self):
        if self._running:
            self.func()
            self._schedule_next()

    def _schedule_next(self):
        self._timer = threading.Timer(3600, self._run)  # 1 hour = 3600 seconds
        self._timer.daemon = True
        self._timer.start()

    def start(self):
        if not self._running:
            self._running = True
            self._schedule_next()
            print("Hourly scheduler started.")

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
            print("Hourly scheduler stopped.")

# Example usage
def my_task():
    print(f"Task executed at {time.ctime()}")

if __name__ == "__main__":
    scheduler = HourlyScheduler(my_task)
    scheduler.start()

    try:
        while True:
            time.sleep(1)  # Keeps the main thread alive
    except KeyboardInterrupt:
        scheduler.stop()
