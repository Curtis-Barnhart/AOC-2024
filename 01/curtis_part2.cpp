#include <fstream>
#include <iostream>
#include <vector>

int main (int argc, char *argv[]) {
    std::ifstream ifs(argv[1]);
    std::vector<unsigned int> llist;
    unsigned int contained[100000] {}, index;

    while (ifs) {
        ifs >> llist.emplace_back();
        ifs >> index;
        ++contained[index];
    }

    int accumulate = 0;
    for (size_t i = 0; i < llist.size(); ++i) {
        accumulate += llist.at(i) * contained[llist.at(i)];
    }
    std::cout << "Solution: " << accumulate << "!\n";

    return 0;
}

