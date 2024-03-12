# linux version (compiler directives for cython compiler)
# distutils: language = c++
# distutils: sources = do_counting.cpp
# distutils: extra_compile_args = -fopenmp -ffast-math -O3
# distutils: extra_link_args = -fopenmp
# cython: language_level = 3

# import numpy 
import numpy as np

from libc.stdint cimport uint32_t,  int32_t, int64_t


cdef extern from "do_counting.h": 
	void do_counting(int32_t * filter_data, 
			uint32_t * distance, 
			uint32_t * direction,
			uint32_t * output) 



def _do_counting(int32_t[:] filter_data, 
		uint32_t [:] distance, 
		uint32_t [:] direction, 
		uint32_t [:] output): 
	do_counting(&filter_data[0], 
			&distance[0], 
			&direction[0], 
			&output[0])


