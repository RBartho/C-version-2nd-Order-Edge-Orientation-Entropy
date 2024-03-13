# C-version-2nd-order edge-orientation entropy

This is a C++ / Cython version of the 2nd order edge orientation entropy originally developed in Python 2 in the following paper: 

### Christoph Redies, Anselm Brachmann, Johan Wagemans,High entropy of edge orientations characterizes visual artworks from diverse cultural backgrounds, Vision Research, Volume 133, 2017, Pages 130-144, https://doi.org/10.1016/j.visres.2017.02.004. ###

The original algorithm is computationally very expensive because it compares the orientation of each edge to every other edge in an image. The C++/Cython version is highly optimized, using parallel execution, (C++ automatic) SIMD instructions, and compiled code. The C++ version has a similar runtime to the Cython version. Compared to the Python 2 version, it is easily possible to archive a speedup of >factor 100 on modern multi-core machines.
