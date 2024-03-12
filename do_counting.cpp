
#include <cstdint>
#include <cmath>
#include <omp.h>
#include <iostream>

void do_counting(const int32_t * filter_data,
                 const uint32_t * distance,
                 const uint32_t * direction,
                 uint32_t * output
                 ) {

    const int32_t num_pixel = 126 * 126;

#pragma omp parallel
    {
        uint32_t diff;
        uint32_t dist;
        uint32_t direc;

        int32_t x_diff;
        int32_t y_diff;

#pragma omp for schedule(dynamic)
        for (int32_t i = 0; i < num_pixel; ++i) {
            for (int32_t t = 0; t < num_pixel; ++t) {


                // calc difference
                diff = abs(filter_data[i] - filter_data[t]);

                // get direction
                y_diff = t / 126 - i / 126;
                x_diff = t % 126 - i % 126;
                direc = direction[(y_diff + 126) + (x_diff + 126) * 252];

                // get distance
                dist = distance[abs(x_diff) + 126 * abs(y_diff)];

#pragma omp atomic
                output[dist + 180 * direc + 180 * 48 * diff] += 1;
            }

        }
    }
}



