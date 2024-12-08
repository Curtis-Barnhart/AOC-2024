#include <cstdio>
#include <fstream>
#include <unordered_set>

#include "../../06/Grid.hpp"

vector<Vec2> antinodes(const Vec2 &a1, const Vec2 &a2, const Grid &g) {
    auto delta = a2 - a1;
    vector<Vec2> ans;
    ans.push_back(a1);
    Vec2 an = a1;
    while (g.on_grid(an = an - delta)) {
        ans.push_back(an);
    }
    an = a1;
    while (g.on_grid(an = an + delta)) {
        ans.push_back(an);
    }
    return ans;
}

int main (int argc, char *argv[]) {
    std::ifstream input("input.txt");
    Grid grid(input);

    std::unordered_set<Vec2> points;

    for (char frequency = '0'; frequency <= '9'; ++frequency) {
        vector<Vec2> locs = grid.all(frequency);
        if (locs.size() < 2) {
            continue;
        }
        for (auto a1 = locs.begin(); a1 < locs.end() - 1; ++a1) {
            // long t1 = a1 < locs.end(),
            //      t2 = std::distance(a1, locs.end()),
            //      t3 = a1 < locs.end() - 1,
            //      t4 = std::distance(a1, locs.end() - 1);
            // std::printf("%ld, %ld, %ld, %ld\n", t1, t2, t3, t4);
            for (auto a2 = a1 + 1; a2 < locs.end(); ++a2) {
                for (const Vec2 &v : antinodes(*a1, *a2, grid)) {
                    if (grid.on_grid(v)) {
                        points.insert(v);
                    }
                }
            }
        }
    }

    for (char frequency = 'A'; frequency <= 'z'; ++frequency) {
        vector<Vec2> locs = grid.all(frequency);
        if (locs.size() < 2) {
            continue;
        }
        for (auto a1 = locs.begin(); a1 < locs.end() - 1; ++a1) {
            for (auto a2 = a1 + 1; a2 < locs.end(); ++a2) {
                for (const Vec2 &v : antinodes(*a1, *a2, grid)) {
                    if (grid.on_grid(v)) {
                        points.insert(v);
                    }
                }
            }
        }
    }
    
    for (const Vec2 &v : points) {
        std::printf("(%d, %d)\n", v.x, v.y);
    }
    std::printf("Part 1 Solution: %ld!\n", points.size());
    return 0;
}

