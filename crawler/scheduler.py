import threading
import time

class HourlyScheduler:
    def __init__(self, seconds, func):
        self.func = func
        self.seconds = seconds
        self._timer = None
        self._running = True
        self.func()  # Run immediately on init
        self._schedule_next()

    def _run(self):
        if self._running:
            self.func()
            self._schedule_next()

    def _schedule_next(self):
        self._timer = threading.Timer(self.seconds, self._run)  # 1 hour = 3600 seconds
        self._timer.daemon = True
        self._timer.start()

    def start(self):
        # ...existing code...
        print("Hourly scheduler started.")

    def stop(self):
        # ...existing code...
        print("Hourly scheduler stopped.")

# # Example usage
# def my_task():
#     print(f"Task executed at {time.localtime()}")

# if __name__ == "__main__":
#     scheduler = HourlyScheduler(my_task)
#     # No need to call start(), already started in __init__
#     try:
#         while True:
#             time.sleep(1)  # Keeps the main thread alive
#     except KeyboardInterrupt:
#         scheduler.stop()
#         time.sleep(1)  # Keeps the main thread alive
#     except KeyboardInterrupt:
#         scheduler.stop()
