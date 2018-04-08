#include <cstdlib>
#include <iostream>

#include "sensing_model_and_map.hpp"

using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char** argv)
{
    cout << "Testing guass()..." << endl;
    cout << "\t" << hmm::gauss(2.0, 3.0, 4.0) << endl;
    cout << "\t" << hmm::gauss(5.5, 4.2, 6.3) << endl;

    cout << "Testing door()..." << endl;
    cout << "\t" << hmm::door(4.4, 2.9) << endl;
    cout << "\t" << hmm::door(1.745, 9.03) << endl;

    cout << "Testing p_door()..." << endl;
    cout << "\t" << hmm::p_door(6.25) << endl;
    cout << "\t" << hmm::p_door(0.23) << endl;

    cout << "Testing p_wall()..." << endl;
    cout << "\t" << hmm::p_wall(2.76) << endl;
    cout << "\t" << hmm:: p_wall(8.2) << endl;

    return EXIT_SUCCESS;
}
