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
    const vector<long>::reverse_iterator &start,
    const vector<long>::reverse_iterator &end,
    long value
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
    {
        auto value_str = "0" + std::to_string(value),
             start_str = std::to_string(*start);
        if (
            value_str.size() >= start_str.size()
            && !value_str.compare(value_str.size() - start_str.size(), start_str.size(), start_str)
            && works(start + 1, end, std::stoll(value_str.substr(0, value_str.size() - start_str.size())))
        ) {
            return true;
        }
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

    vector<vector<long>> numbers;
    vector<long> values;

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

    long acc = 0;
    for (size_t x = 0; x < numbers.size(); ++x) {
        if (works(numbers.at(x).rbegin(), numbers.at(x).rend(), values.at(x))) {
            acc += values.at(x);
        }
    }

    std::printf("Solution: %ld!\n", acc);

    return 0;
}


