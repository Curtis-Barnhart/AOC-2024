#include <algorithm>
#include <cassert>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>

int main (int argc, char *argv[]) {
    std::ifstream ifs(argv[1]);
    std::vector<int> llist, rlist;

    while (ifs) {
        llist.push_back(0);
        rlist.push_back(0);
        ifs >> llist.back();
        ifs >> rlist.back();
    }

    std::sort(llist.begin(), llist.end());
    std::sort(rlist.begin(), rlist.end());

    int accumulate = 0;
    for (size_t i = 0; i < llist.size(); i++) {
        accumulate += std::abs(llist.at(i) - rlist.at(i));
    }
    std::cout << "Solution: " << accumulate << "!\n";

    return 0;
}

