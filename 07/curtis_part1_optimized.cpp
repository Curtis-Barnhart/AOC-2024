#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

using std::vector;

bool works(
    const vector<long long>::reverse_iterator &start,
    const vector<long long>::reverse_iterator &end,
    long long value
) {
    if (std::distance(start, end) == 1) {
        return *start == value;
    }
    if (
        value % *start == 0
        && works(start + 1, end, value / *start)
    ) {
        return true;
    }
    return works(
        start + 1,
        end,
        value - *start
    );
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    std::string s;

    vector<vector<long long>> numbers;
    vector<long long> values;

    while (std::getline(input, s)) {
        std::stringstream stream(s);
        numbers.emplace_back();

        stream >> values.emplace_back();
        stream.seekg(1, std::ios_base::cur);

        while (stream) {
            stream >> numbers.back().emplace_back();
        }
        numbers.back().pop_back();
    }

    long long acc = 0;
    for (size_t x = 0; x < numbers.size(); ++x) {
        if (works(numbers.at(x).rbegin(), numbers.at(x).rend(), values.at(x))) {
            acc += values.at(x);
        }
    }

    std::printf("Solution: %lld!\n", acc);

    return 0;
}


