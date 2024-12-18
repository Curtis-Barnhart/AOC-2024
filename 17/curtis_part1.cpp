#include <cassert>
#include <cstdio>
#include <vector>

int combo(int x, long REG_A, long REG_B, long REG_C) {
    assert(x >= 0 && x <= 7);
    switch (x) {
        case 4:
            return REG_A;
        case 5:
            return REG_B;
        case 6:
            return REG_C;
        case 7:
            throw 7;
        default:
            return x;
    }
}

void simulate(
    const std::vector<int> &code,
    std::vector<int> &out,
    long REG_A
) {
    long REG_B = 0, REG_C = 0, PC = 0;
    while (PC < code.size()) {
        switch (code.at(PC)) {
            case 0x00:
                REG_A = REG_A >> combo(code.at(PC + 1), REG_A, REG_B, REG_C);
                PC += 2;
                break;
            case 0x01:
                REG_B ^= code.at(PC + 1);
                PC += 2;
                break;
            case 0x02:
                REG_B = 0x07 & combo(code.at(PC + 1), REG_A, REG_B, REG_C);
                PC += 2;
                break;
            case 0x03:
                if (REG_A) {
                    PC = code.at(PC + 1);
                } else {
                    PC += 2;
                }
                break;
            case 0x04:
                REG_B = REG_B ^ REG_C;
                PC += 2;
                break;
            case 0x05:
                out.push_back(combo(code.at(PC + 1), REG_A, REG_B, REG_C) & 0x07);
                PC += 2;
                break;
            case 0x06:
                REG_B = REG_A >> combo(code.at(PC + 1), REG_A, REG_B, REG_C);
                PC += 2;
                break;
            case 0x07:
                REG_C = REG_A >> combo(code.at(PC + 1), REG_A, REG_B, REG_C);
                PC += 2;
                break;
        }
    }
}

int main (int argc, char *argv[]) {
    std::vector<int> code { 2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0 }, out;
    // simulate(code, out, 44374556);
    simulate(code, out, 105981155568026);

    std::printf("Solution: ");
    for (auto begin = out.begin(); begin < std::prev(out.end()); ++begin) {
        std::printf("%d,", *begin);
    }
    std::printf("%d!\n", *(std::prev(out.end())));
}

