import time


class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.running = False
        self.stop_time = None
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()
        self.running = True

    def split(self):
        self.stop_time = time.time()
        self.elapsed_time = self.stop_time - self.start_time

    def stop(self):
        self.split()
        self.running = False

    def countdown_to(self, seconds):
        if self.elapsed_time > seconds:
            self.stop()
            return True

        if not self.running:
            self.start()
        else:
            self.split()

        return False
