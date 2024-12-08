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

long long pow10(int exp) {
    assert(exp >= 0);
    if (exp == 0) {
        return 1;
    }
    long long acc = 1;
    while (exp-->0) {
        acc *= 10;
    }
    return acc;
}

long long evaluate(const vector<long long> &nums, const vector<ops> &operators) {
    long long acc = nums.at(0);
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

bool works(const vector<long long> &nums, long long value) {
    OpGenerator gen(nums.size() - 1);
    vector<ops> operators;
    
    while (gen.next(operators)) {
        if (evaluate(nums, operators) == value) {
            return true;
        }
    }
    return false;
}

/*
* Tried values:
* 563590806965177 (too low)
* 581941094529163 (correct)
*/
int main (int argc, char *argv[]) {
    std::ifstream input("./input.txt");
    std::string s;

    vector<vector<long long>> numbers;
    numbers.reserve(850);
    vector<long long> values;
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

    long long acc = 0;
    int total_work = 0;
    for (size_t x = 0; x < numbers.size(); ++x) {
        if (works(numbers.at(x), values.at(x))) {
            printf("%3zu = %14lld works!\n", x, values.at(x));
            acc += values.at(x);
            ++total_work;
        }
    }

    std::printf("Total working: %d!\n", total_work);
    std::printf("Solution: %lld!\n", acc);

    return 0;
}

