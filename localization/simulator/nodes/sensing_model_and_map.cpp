#include "sensing_model_and_map.hpp"

namespace hmm
{
    float gauss(float x, float mu, float sigma)
    {
        float exp = 0 - (std::pow((x-mu), 2) / (2 * sigma * sigma));
        return (1/(sigma * std::sqrt(2*M_PI))) * (std::pow(M_E, exp));
    }

    float door(float mu, float x)
    {
        float sigma = 0.75;
        float peak = gauss(0, 0, sigma);   
        return 0.8 * gauss(x, mu, sigma)/peak;
    }

    float p_door(float x)
    {
        return 0.1 + door(11, x) + door(18.5, x) + door(41, x);
    }
    
    float p_wall(float x)
    {
        return 1.0 - p_door(x);
    }

}
