import unittest

from logger import log_time


class DatasetTest(unittest.TestCase):

    @log_time
    def test_perf_of_threaded_io(self):
        import math
        import pyximport
        pyximport.install()
        from python_perf.cython_extension import demo as cython_demo
        from python_perf.c_extension import demo as c_demo

        @log_time  # 2.04s
        def heavy_calculation():
            a = 0
            pow = math.pow
            for i in range(10000000):
                a += pow(2, 10)
            return a

        @log_time  # 0.028s
        def heavy_calculation_in_c():
            c_demo.pure_heavy_calculation()

        @log_time  # 0.01s
        def heavy_calculation_in_cython():
            cython_demo.heavy_calculation()

        @log_time  # 0.5s
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

        heavy_calculation()
        heavy_calculation_in_c()
        heavy_calculation_in_cython()
