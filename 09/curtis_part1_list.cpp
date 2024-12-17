#include <cassert>
#include <cstdio>
#include <fstream>
#include <list>

struct MBlock {
    int id = 0, size = 0;
};

void sum_left(const std::list<MBlock>::iterator &b, long &loc, long &cumulative_sum) {
    cumulative_sum += (b->id * (loc*b->size + (b->size)*(b->size - 1)/2));
    loc += b->size;
}

std::list<MBlock> read_blocks(char *argv[]) {
    std::list<MBlock> blocks;
    std::ifstream input(argv[1]);

    int empty = 0, id = 0;
    char c;
    while (input >> c) {
        c -= '0';
        blocks.push_back({ empty ? -1 : id++, c });
        empty = !empty;
    }
    return blocks;
}

int main(int argc, char *argv[]) {
    std::list<MBlock> blocks = read_blocks(argv);
    long cumulative_sum = 0, loc = 0;
    std::list<MBlock>::iterator head = blocks.begin(), tail = --blocks.end();

    while (head != tail) {
        if (head->size) {
            if (head->id >= 0) {
                sum_left(head++, loc, cumulative_sum);
            } else {
                if (tail->id >= 0) {
                    if (tail->size <= head->size) {
                        head->size -= tail->size;
                        sum_left(tail--, loc, cumulative_sum);
                    } else {
                        head->id = tail->id;
                        tail->size -= head->size;
                        sum_left(head++, loc, cumulative_sum);
                    }
                } else {
                    --tail;
                }
            }
        } else {
            ++head;
        }
    }

    if (head->id >= 0) {
        sum_left(head, loc, cumulative_sum);
    }

    std::printf("Solution: %ld!\n", cumulative_sum);
    return 0;
}

