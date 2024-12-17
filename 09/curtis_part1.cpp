#include <cassert>
#include <cstdio>
#include <fstream>
#include <string>

int main (int argc, char *argv[]) {
    long checksum = 0;
    std::ifstream input(argv[1]);
    std::string s;
    input >> s;
    
    if (s.size() % 2 != 1) {
        s.append(1, '0');
    }
    long left_block = 0, rite_block = s.size() - 1,
        loc = 0,
        left_free_rem = 0,
        left_file_rem = s.at(left_block) - '0',
        rite_file_rem = s.at(rite_block) - '0';

    while (left_block != rite_block) {
        if (left_block % 2) {
            // if we are on a free block on the left
            if (left_free_rem) {
                // and there is still free space here
                if (rite_block % 2) {
                    // but there is also free space on the right
                    --rite_block;
                    rite_file_rem = s.at(rite_block) - '0';
                    // then remove all the free space on the right.
                } else {
                    // and there is a file to read on the right
                    if (rite_file_rem) {
                        // if that file is not empty
                        --rite_file_rem;
                        --left_free_rem;
                        checksum += loc++ * (rite_block / 2);
                        // then read one piece from it and continue
                    } else {
                        // but that file is actually empty
                        --rite_block;
                        // then decrement the right counter and load in right free
                    }
                }
            } else {
                // and we have run out of free space
                ++left_block;
                left_file_rem = s.at(left_block) - '0';
                // then increment the left counter and load in the left file
            }
        } else {
            // if we are on a file block on the left
            if (left_file_rem) {
                // and there is file left to read
                checksum += loc++ * (left_block / 2);
                --left_file_rem;
                // then read one step of it.
            } else {
                // and we have run out of file
                ++left_block;
                left_free_rem = s.at(left_block) - '0';
                // then increment the block and load in the free space counter.
            }
        }
    }

    if (!(left_block % 2)) {
        // if we are on a file
        int remaining = left_file_rem + rite_file_rem - (s.at(left_block) - '0');
        assert(remaining >= 0);
        while (remaining-->0) {
            checksum += loc++ * (left_block / 2);
        }
    }

    std::printf("Solution: %ld!\n", checksum);
    return 0;
}

