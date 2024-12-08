#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

int main (int argc, char *argv[]) {
    std::ifstream ifs(argv[1]);
    std::vector<int> llist, rlist;

    while (ifs) {
        ifs >> llist.emplace_back();
        ifs >> rlist.emplace_back();
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

