#include <cassert>
#include <cstdio>
#include <vector>

struct VM_State {
    long REG_A, REG_B, REG_C, PC;
};

long combo(int x, VM_State &vm) {
    assert(x >= 0 && x <= 7);
    switch (x) {
        case 4:
            return vm.REG_A;
        case 5:
            return vm.REG_B;
        case 6:
            return vm.REG_C;
        case 7:
            throw 7;
        default:
            return x;
    }
}

int simulate_until_out(
    const std::vector<int> &code,
    VM_State &vm
) {
    int return_val;
    while (vm.PC < code.size()) {
        switch (code.at(vm.PC)) {
            case 0x00:
                vm.REG_A = vm.REG_A >> combo(code.at(vm.PC + 1), vm);
                vm.PC += 2;
                break;
            case 0x01:
                vm.REG_B ^= code.at(vm.PC + 1);
                vm.PC += 2;
                break;
            case 0x02:
                vm.REG_B = 0x07 & combo(code.at(vm.PC + 1), vm);
                vm.PC += 2;
                break;
            case 0x03:
                if (vm.REG_A) {
                    vm.PC = code.at(vm.PC + 1);
                } else {
                    vm.PC += 2;
                }
                break;
            case 0x04:
                vm.REG_B = vm.REG_B ^ vm.REG_C;
                vm.PC += 2;
                break;
            case 0x05:
                return_val = combo(code.at(vm.PC + 1), vm) & 0x07;
                vm.PC += 2;
                return return_val;
            case 0x06:
                vm.REG_B = vm.REG_A >> combo(code.at(vm.PC + 1), vm);
                vm.PC += 2;
                break;
            case 0x07:
                vm.REG_C = vm.REG_A >> combo(code.at(vm.PC + 1), vm);
                vm.PC += 2;
                break;
        }
    }
    return -1;
}

long has_solution(
    int segments_left,
    const std::vector<int> &code,
    long REG_A
) {
    if (segments_left) {
        for (long x = 0; x < 8; ++x) {
            VM_State copy{(REG_A << 3) | x, 0, 0, 0};
            if (simulate_until_out(code, copy) == code.at(segments_left - 1)) {
                long next_step = has_solution(segments_left - 1, code, (REG_A << 3) | x);
                if (next_step != -1) {
                    return next_step;
                }
            }
        }
        return -1;
    } else {
        return REG_A;
    }
}

int main (int argc, char *argv[]) {
    std::vector<int> code { 2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0 }, out;
    long solution = has_solution(16, code, 0);
    std::printf("Solution: %ld!\n", solution);
}

