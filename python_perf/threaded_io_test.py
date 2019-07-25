import unittest

from logger import log_time


class DatasetTest(unittest.TestCase):

    @log_time
    def test_perf_of_threaded_io(self):

        @log_time
        def heavy_calculation():
            import math
            a = 0
            for i in range(10000000):
                a += math.pow(2, 10)

        @log_time
        def heavy_io():
            open(r'some-600M-file', 'rb').read()

        @log_time
        def exec_in_single_thread():
            heavy_calculation()
            heavy_io()

        @log_time
        def exec_in_multi_thread():
            from threading import Thread

            threads = [Thread(target=heavy_calculation), Thread(target=heavy_io)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        exec_in_single_thread()
        exec_in_multi_thread()
