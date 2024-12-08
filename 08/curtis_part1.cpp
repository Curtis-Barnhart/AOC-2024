#include <cassert>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <unordered_set>

#include "../06/curtis_grid.hpp"

vector<Vec2> antinodes(const Vec2 &a1, const Vec2 &a2) {
    auto delta = a2 - a1;
    return { {a1 - delta}, {a2 + delta} };
}

int main (int argc, char *argv[]) {
    std::ifstream input("input.txt");
    Grid grid(input);

    std::unordered_set<Vec2> points;

    char frequencies[62], *where = frequencies;
    for (char c = '0'; c <= '9'; ++c) {
        *(where++) = c;
    }
    for (char c = 'A'; c <= 'Z'; ++c) {
        *(where++) = c;
    }
    for (char c = 'a'; c <= 'z'; ++c) {
        *(where++) = c;
    }

    for (char frequency: frequencies) {
        vector<Vec2> locs = grid.all(frequency);
        if (locs.size() > 1) {
            for (auto a1 = locs.begin(); a1 < locs.end() - 1; ++a1) {
                for (auto a2 = a1 + 1; a2 < locs.end(); ++a2) {
                    for (const Vec2 &v : antinodes(*a1, *a2)) {
                        if (grid.on_grid(v)) {
                            points.insert(v);
                        }
                    }
                }
            }
        }
    }

    std::printf("Part 1 Solution: %ld!\n", points.size());
    return 0;
}

