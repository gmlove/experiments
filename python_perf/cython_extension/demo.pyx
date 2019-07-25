from libc.math cimport pow

def heavy_calculation():
    import math
    cdef double a = 0
    cdef int i
    with nogil:
        for i in range(10000000):
            a += pow(2, 10)
    return a
