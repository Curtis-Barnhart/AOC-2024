#include <cstdio>
#include <fstream>
#include <unordered_set>

#include "../06/curtis_grid.hpp"

vector<Vec2> valid_neighbors(const Vec2 &loc, const Grid &g) {
    vector<Vec2> neighbors;
    if (g.on_grid(loc + Vec2(1, 0))) {
        neighbors.push_back(loc + Vec2(1, 0));
    }
    if (g.on_grid(loc + Vec2(0, 1))) {
        neighbors.push_back(loc + Vec2(0, 1));
    }
    if (g.on_grid(loc + Vec2(-1, 0))) {
        neighbors.push_back(loc + Vec2(-1, 0));
    }
    if (g.on_grid(loc + Vec2(0, -1))) {
        neighbors.push_back(loc + Vec2(0, -1));
    }
    return neighbors;
}

int th_score(const Vec2 &th, const Grid &g) {
    std::unordered_set<Vec2> visited;
    vector<Vec2> stack;
    visited.insert(th);
    stack.push_back(th);
    int score = 0;

    while (!stack.empty()) {
        Vec2 next = stack.back();
        stack.pop_back();

        if (g.at(next) == '9') {
            ++score;
        } else {
            vector<Vec2> neighbors = valid_neighbors(next, g);
            for (const Vec2 &n : neighbors) {
                if (
                    visited.find(n) == visited.end()
                    && g.at(n) - g.at(next) == 1
                ) {
                    visited.insert(n);
                    stack.push_back(n);
                }
            }
        }
    }

    return score;
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(input);

    int score_sum = 0;
    vector<Vec2> trailheads = grid.all('0');
    for (const Vec2 &th : trailheads) {
        score_sum += th_score(th, grid);
    }

    std::printf("Solution: %d!\n", score_sum);
    return 0;
}

