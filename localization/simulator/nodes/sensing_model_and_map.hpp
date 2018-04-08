#include <cmath>

namespace hmm
{
    // definition of normal curve
    float gauss(float x, float mu, float sigma);

    // this experimentally approximates door sensor performance
    float door(float mu, float x);

    // doors are centered at 11m, 18.5m, and 41m
    float p_door(float x);
    
    //
    float p_wall(float x);

}
