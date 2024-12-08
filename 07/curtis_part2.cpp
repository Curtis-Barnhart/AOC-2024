#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <vector>

using std::vector;

enum ops { ADD, MUL, CAT };

long evaluate(const vector<long> &nums, const vector<ops> &operators) {
    long acc = nums.at(0);
    auto current_num = nums.begin();
    auto current_op = operators.begin();
    while (++current_num < nums.end()) {
        switch (*current_op) {
            case ADD:
                acc += *current_num;
                break;
            case MUL:
                acc *= *current_num;
                break;
            case CAT:
                {
                    std::stringstream catter;
                    catter << acc << *current_num;
                    catter >> acc;
                }
                break;
        }
        ++current_op;
    }

    return acc;
}

struct OpGenerator {
    vector<ops> operators;
    bool valid = true;

    OpGenerator(int size) {
        while (size-->0) {
            this->operators.push_back(ADD);
        }
    }

    bool next(vector<ops> &output) {
        if (!this->valid) {
            return false;
        }
        output = this->operators;
        int x = this->operators.size();
        while (--x >= 0) {
            switch (this->operators.at(x)) {
                case ADD:
                    this->operators.at(x) = MUL;
                    goto increment_done;
                    break;
                case MUL:
                    this->operators.at(x) = CAT;
                    goto increment_done;
                    break;
                case CAT:
                    this->operators.at(x) = ADD;
                    break;
            }
        }
        increment_done:
        this->valid = x >= 0;
        return true;
    }
};

bool works(const vector<long> &nums, long value) {
    OpGenerator gen(nums.size() - 1);
    vector<ops> operators;
    
    while (gen.next(operators)) {
        if (evaluate(nums, operators) == value) {
            return true;
        }
    }
    return false;
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    std::string s;

    vector<vector<long>> numbers;
    numbers.reserve(850);
    vector<long> values;
    values.reserve(850);

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
        if (works(numbers.at(x), values.at(x))) {
            acc += values.at(x);
        }
    }

    std::printf("Solution: %ld!\n", acc);

    return 0;
}

