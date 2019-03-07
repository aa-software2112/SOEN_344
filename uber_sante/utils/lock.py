import threading


class ReadWriteLock:
    """
    An implementation of a lock based on the Readers-Writers Problem #4
    A process can read if there are no writers in and no writers waiting.
    A process can write if there are no readers reading and no writers writing.
    """

    def __init__(self):
        self._rw_lock = threading.Condition(threading.Lock())
        self._lock = threading.Lock()
        self._num_of_readers = 0
        self._readers_waiting = 0
        self._writers_waiting = 0

    def start_read(self):
        with self._lock:
            self._readers_waiting += 1

        self._rw_lock.acquire()

        while self._writers_waiting > 0:
            self._rw_lock.wait()
        try:
            self._num_of_readers += 1
            self._readers_waiting -= 1
        finally:
            self._rw_lock.release()

    def end_read(self):
        self._rw_lock.acquire()
        try:
            self._num_of_readers -= 1
            if self._num_of_readers == 0:
                self._rw_lock.notify_all()
        finally:
            self._rw_lock.release()

    def start_write(self):
        with self._lock:
            self._writers_waiting += 1

        self._rw_lock.acquire()

        while self._num_of_readers > 0:
            self._rw_lock.wait()

        self._writers_waiting -= 1

    def end_write(self):
        try:
            self._rw_lock.notify_all()
        finally:
            self._rw_lock.release()


# For testing purposes.
if __name__ == '__main__':
    import time

    rwl = ReadWriteLock()


    class Reader(threading.Thread):
        def run(self):
            print(self, 'start')
            rwl.start_read()
            print(self, 'acquired')
            time.sleep(5)
            print(self, 'stop')
            rwl.end_read()


    class Writer(threading.Thread):
        def run(self):
            print(self, 'start')
            rwl.start_write()
            print(self, 'acquired')
            time.sleep(10)
            print(self, 'stop')
            rwl.end_write()


    Reader().start()
    time.sleep(1)
    Reader().start()
    time.sleep(1)
    Reader().start()
    time.sleep(1)
    Writer().start()
    time.sleep(3)
    Reader().start()
    Writer().start()
    Writer().start()
    Writer().start()
    Reader().start()
    Writer().start()
    Reader().start()
    Reader().start()