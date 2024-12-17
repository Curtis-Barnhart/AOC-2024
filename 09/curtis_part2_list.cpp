#include <algorithm>
#include <cassert>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <list>

struct MBlock {
    int id = 0, size = 0;
};

typedef std::list<MBlock>::iterator MListIter;

std::list<MBlock> read_blocks(char *argv[]) {
    std::list<MBlock> blocks;
    std::ifstream input(argv[1]);

    int empty = 0, id = 0;
    char c;
    // while the chars keep coming, put them at the back of the list of blocks
    // empty tracks whether the block contains a file or is free
    while (input >> c) {
        c -= '0';
        blocks.push_back({ empty ? -1 : id++, c });
        empty = !empty;
    }
    return blocks;
}

void remove_empty(
    std::list<MBlock> &blocks
) {
    // first remove all empty places
    blocks.remove_if([](const MBlock &b){ return b.size == 0; });
    // then we stitch together any free spaces next to each other
    auto it = blocks.begin(), next = std::next(it);
    while (next != blocks.end()) {
        if (it->id < 0 && next->id < 0) {
            it->size += next->size;
            blocks.erase(next);
            next = std::next(it);
        } else {
            std::advance(it, 1);
            std::advance(next, 1);
        }
    }
}

void shift_blocks(std::list<MBlock> &blocks) {
    MListIter cur_b = std::prev(blocks.end());
    int next_id = cur_b->id;
    // we count backwards until we run out of blocks
    while (cur_b != blocks.begin()) {
        if (cur_b->id != next_id) {
            std::advance(cur_b, -1);
        } else {
            --next_id;
            // if we're looking at a file block, find the first place it can go
            MListIter inserter = std::find_if(
                blocks.begin(), cur_b,
                [=](const MBlock &b){ return b.id < 0 && b.size >= cur_b->size; }
            );
            if (inserter != cur_b) {
                // insert new block before free space (and opt remove free space)
                blocks.insert(inserter, {cur_b->id, cur_b->size});
                if (inserter->size == cur_b->size) {
                    blocks.erase(inserter);
                } else {
                    inserter->size -= cur_b->size;
                }

                // remove old block (and opt combine free space surrounding)
                MListIter rem_prev = std::prev(cur_b),
                          rem_next = std::next(cur_b);
                cur_b->id = -1;
                if (rem_prev->id < 0) {
                    cur_b->size += rem_prev->size;
                    blocks.erase(rem_prev);
                }
                if (rem_next != blocks.end() && rem_next->id < 0) {
                    cur_b->size += rem_next->size;
                    blocks.erase(rem_next);
                }
            }
        }
    }
}

int main (int argc, char *argv[]) {
    long cumulative_sum = 0, loc = 0;
    std::list<MBlock> blocks = read_blocks(argv);
    remove_empty(blocks);
    shift_blocks(blocks);
    for (const MBlock &b : blocks) {
        if (b.id >= 0) {
            cumulative_sum += (b.id * (loc*b.size + (b.size)*(b.size - 1)/2));
        }
        loc += b.size;
    }

    std::printf("Solution: %ld!\n", cumulative_sum);
    return 0;
}

