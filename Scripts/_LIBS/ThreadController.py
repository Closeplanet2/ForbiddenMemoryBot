import threading
import asyncio

class ThreadController:
    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.loaded_threads = []

    def load_start(self, method, daemon, *args):
        self.load_threads(method, daemon, args)
        self.start_all_threads()

    def load_start_wait(self, method, daemon, *args):
        self.load_threads(method, daemon, args)
        self.start_all_threads()
        self.wait_for_all_threads()

    def load_threads(self, method, daemon, *args):
        for index in range(0, self.max_threads, 1):
            thread = threading.Thread(target=method, args=(index, args,))
            thread.daemon = daemon
            self.loaded_threads.append(thread)

    def start_all_threads(self):
        for thread in self.loaded_threads:
            thread.start()

    def wait_for_all_threads(self):
        for thread in self.loaded_threads:
            thread.join()